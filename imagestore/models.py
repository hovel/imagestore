import uuid
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
    from places.models import GeoPlace
except:
    GeoPlace = None

UPLOAD_TO = getattr(settings, 'IMAGESTORE_UPLOAD_TO', 'imagestore/')
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
    name = models.CharField(_('Name'), max_length=20, blank=False, null=False)
    created = models.DateTimeField(_('Created'), auto_now_add=True)
    updated = models.DateTimeField(_('Updated'), auto_now=True)
    is_public = models.BooleanField(_('Is public'), default=True)
    head = models.ForeignKey('Image', related_name='head_of', null=True, blank=True)

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
        
    title = models.CharField(_('Title'), max_length=20, blank=True, null=True)
    description = models.TextField(_('Description'), blank=True, null=True)
    tags = TagField(_('Tags'), blank=True)
    order = models.IntegerField(_('Order'), null=False, blank=False, default=0)
    image = ImageField(verbose_name = _('File'), upload_to=get_file_path)
    user = models.ForeignKey(User, verbose_name=_('User'), null=True, blank=True, related_name='images')
    created = models.DateTimeField(_('Created'), auto_now_add=True, null=True)
    updated = models.DateTimeField(_('Updated'), auto_now=True, null=True)
    album = models.ForeignKey(Album, verbose_name=_('Album'), null=True, blank=True, related_name='images')

    @permalink
    def get_absolute_url(self):
        return 'imagestore:image', (), {'pk': self.id}

    def __unicode__(self):
        return self.title

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


#noinspection PyUnusedLocal
def setup_imagestore_permissions(instance, created, **kwargs):
        if not created:
            return
        try:
            add_image_permission = Permission.objects.get(codename='add_image', content_type__name='Image')
            add_album_permission = Permission.objects.get(codename='add_album', content_type__name='Album')
            change_image_permission = Permission.objects.get(codename='change_image', content_type__name='Image')
            change_album_permission = Permission.objects.get(codename='change_album', content_type__name='Album')
            delete_image_permission = Permission.objects.get(codename='delete_image', content_type__name='Image')
            delete_album_permission = Permission.objects.get(codename='delete_album', content_type__name='Album')
        except Permission.DoesNotExist:
            pass
        instance.user_permissions.add(add_image_permission, add_album_permission,)
        instance.user_permissions.add(change_image_permission, change_album_permission,)
        instance.user_permissions.add(delete_image_permission, delete_album_permission,)

if SELF_MANAGE:
    post_save.connect(setup_imagestore_permissions, User)