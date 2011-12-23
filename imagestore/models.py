import uuid
import zipfile
from django.core.files.base import ContentFile
import os

from django.db import models
from django.db.models import permalink
from sorl.thumbnail.helpers import ThumbnailError
from tagging.fields import TagField
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from sorl.thumbnail import ImageField, get_thumbnail
from django.contrib.auth.models import User, Permission
from django.db.models.signals import post_save
try:
    import Image as PILImage
except ImportError:
    from PIL import Image as PILImage

try:
    from places.models import GeoPlace
except ImportError:
    GeoPlace = None


UPLOAD_TO = getattr(settings, 'IMAGESTORE_UPLOAD_TO', 'imagestore/')
TEMP_DIR = getattr(settings, 'TEMP_DIR', 'temp/')
SELF_MANAGE = getattr(settings, 'IMAGESTORE_SELF_MANAGE', True)

#noinspection PyUnusedLocal
def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join(UPLOAD_TO, filename)

class Album(models.Model):
    class Meta(object):
        verbose_name = _('Album')
        verbose_name_plural = _('Albums')
        ordering = ('created', 'name')
        permissions = (
            ('moderate_albums', 'View, update and delete any album'),
        )

    user = models.ForeignKey(User, verbose_name=_('User'), null=True, blank=True, related_name='albums')
    name = models.CharField(_('Name'), max_length=100, blank=False, null=False)
    created = models.DateTimeField(_('Created'), auto_now_add=True)
    updated = models.DateTimeField(_('Updated'), auto_now=True)
    is_public = models.BooleanField(_('Is public'), default=True)
    head = models.ForeignKey('Image', related_name='head_of', null=True, blank=True)

    order = models.IntegerField(_('Order'), default=0)

    def get_head(self):
        if self.head:
            return self.head
        else:
            if self.images.all().count()>0:
                self.head = self.images.all()[0]
                self.save()
                return self.head
            else:
                return None

    @permalink
    def get_absolute_url(self):
        return 'imagestore:album', (), {'album_id': self.id}

    def __unicode__(self):
        return self.name

    def admin_thumbnail(self):
        img = self.get_head()
        if img:
            try:
                return '<img src="%s">' % get_thumbnail(img.image, '100x100', crop='center').url
            except IOError:
                return 'IOError'
        return _('Empty album')

    admin_thumbnail.short_description = _('Head')
    admin_thumbnail.allow_tags = True
    

class Image(models.Model):
    class Meta(object):
        verbose_name = _('Image')
        verbose_name_plural = _('Images')
        ordering = ('order', 'id')
        permissions = (
            ('moderate_images', 'View, update and delete any image'),
        )
        
    title = models.CharField(_('Title'), max_length=100, blank=True, null=True)
    description = models.TextField(_('Description'), blank=True, null=True)
    tags = TagField(_('Tags'), blank=True)
    order = models.IntegerField(_('Order'), default=0)
    image = ImageField(verbose_name = _('File'), upload_to=get_file_path)
    user = models.ForeignKey(User, verbose_name=_('User'), null=True, blank=True, related_name='images')
    created = models.DateTimeField(_('Created'), auto_now_add=True, null=True)
    updated = models.DateTimeField(_('Updated'), auto_now=True, null=True)
    album = models.ForeignKey(Album, verbose_name=_('Album'), null=True, blank=True, related_name='images')

    @permalink
    def get_absolute_url(self):
        return 'imagestore:image', (), {'pk': self.id}

    def __unicode__(self):
        return '%s'% self.id

    def admin_thumbnail(self):
        try:
            return '<img src="%s">' % get_thumbnail(self.image, '100x100', crop='center').url
        except IOError:
            return 'IOError'
        except ThumbnailError, ex:
            return 'ThumbnailError, %s' % ex.message
        
    admin_thumbnail.short_description = _('Thumbnail')
    admin_thumbnail.allow_tags = True

if GeoPlace:
    field = models.ForeignKey(GeoPlace, verbose_name=_('Place'), null=True, blank=True, related_name='images')
    field.contribute_to_class(Image, 'place')


class AlbumUpload(models.Model):
    """
    Just re-written django-photologue GalleryUpload method
    """
    zip_file = models.FileField(_('images file (.zip)'), upload_to=TEMP_DIR,
                                help_text=_('Select a .zip file of images to upload into a new Gallery.'))
    album = models.ForeignKey(
        Album, null=True, blank=True,
        help_text=_('Select an album to add these images to. leave this empty to create a new album from the supplied title.')
    )
    new_album_name = models.CharField(max_length=255, blank=True, verbose_name=_('New album name'))
    tags = models.CharField(max_length=255, blank=True, verbose_name=_('tags'))

    class Meta(object):
        verbose_name = _('Album upload')
        verbose_name_plural = _('Album uploads')

    def save(self, *args, **kwargs):
        super(AlbumUpload, self).save(*args, **kwargs)
        album = self.process_zipfile()
        super(AlbumUpload, self).delete()
        return album

    def process_zipfile(self):
        if os.path.isfile(self.zip_file.path):
            # TODO: implement try-except here
            zip = zipfile.ZipFile(self.zip_file.path)
            bad_file = zip.testzip()
            if bad_file:
                raise Exception('"%s" in the .zip archive is corrupt.' % bad_file)
            count = 1
            album = self.album
            if not album:
                album = Album.objects.create(name=self.new_album_name)
            from cStringIO import StringIO
            for filename in sorted(zip.namelist()):
                if filename.startswith('__'): # do not process meta files
                    continue
                data = zip.read(filename)
                if len(data):
                    try:
                        # the following is taken from django.newforms.fields.ImageField:
                        #  load() is the only method that can spot a truncated JPEG,
                        #  but it cannot be called sanely after verify()
                        trial_image = PILImage.open(StringIO(data))
                        trial_image.load()
                        # verify() is the only method that can spot a corrupt PNG,
                        #  but it must be called immediately after the constructor
                        trial_image = PILImage.open(StringIO(data))
                        trial_image.verify()
                    except Exception:
                        # if a "bad" file is found we just skip it.
                        continue
                    img = Image(album=album)
                    img.image.save(filename, ContentFile(data))
                    img.save()
            zip.close()
            return album

#noinspection PyUnusedLocal
def setup_imagestore_permissions(instance, created, **kwargs):
        if not created:
            return
        try:
            add_image_permission = Permission.objects.get_by_natural_key('add_image', 'imagestore', 'image')
            add_album_permission = Permission.objects.get_by_natural_key('add_album', 'imagestore', 'album')
            change_image_permission = Permission.objects.get_by_natural_key('change_image', 'imagestore', 'image')
            change_album_permission = Permission.objects.get_by_natural_key('change_album', 'imagestore', 'album')
            delete_image_permission = Permission.objects.get_by_natural_key('delete_image', 'imagestore','image')
            delete_album_permission = Permission.objects.get_by_natural_key('delete_album', 'imagestore', 'album')
            instance.user_permissions.add(add_image_permission, add_album_permission,)
            instance.user_permissions.add(change_image_permission, change_album_permission,)
            instance.user_permissions.add(delete_image_permission, delete_album_permission,)
        except Permission.DoesNotExist:
            pass


if SELF_MANAGE:
    post_save.connect(setup_imagestore_permissions, User)