#!/usr/bin/env python
# vim:fileencoding=utf-8

__author__ = 'zeus'


from django.db import models
from django.db.models import permalink
from sorl.thumbnail.helpers import ThumbnailError
from tagging.fields import TagField
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from sorl.thumbnail import ImageField, get_thumbnail
from django.contrib.auth.models import User, Permission
from django.db.models.signals import post_save
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist

try:
    import Image as PILImage
except ImportError:
    from PIL import Image as PILImage

from imagestore.utils import get_file_path, get_model_string, load_class



SELF_MANAGE = getattr(settings, 'IMAGESTORE_SELF_MANAGE', True)


class BaseImage(models.Model):
    class Meta(object):
        abstract = True
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
    album = models.ForeignKey(get_model_string('Album'), verbose_name=_('Album'), null=True, blank=True, related_name='images')

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


#noinspection PyUnusedLocal
def setup_imagestore_permissions(instance, created, **kwargs):
        if not created:
            return
        try:
            from imagestore.models import Album, Image
            album_type = ContentType.objects.get(
                #app_label=load_class('imagestore.models.Album')._meta.app_label,
                app_label = Album._meta.app_label,
                name='Album'
            )
            image_type = ContentType.objects.get(
                #app_label=load_class('imagestore.models.Image')._meta.app_label,
                app_label = Image._meta.app_label,
                name='Image'
            )
            add_image_permission = Permission.objects.get(codename='add_image', content_type=image_type)
            add_album_permission = Permission.objects.get(codename='add_album', content_type=album_type)
            change_image_permission = Permission.objects.get(codename='change_image', content_type=image_type)
            change_album_permission = Permission.objects.get(codename='change_album', content_type=album_type)
            delete_image_permission = Permission.objects.get(codename='delete_image', content_type=image_type)
            delete_album_permission = Permission.objects.get(codename='delete_album', content_type=album_type)
            instance.user_permissions.add(add_image_permission, add_album_permission,)
            instance.user_permissions.add(change_image_permission, change_album_permission,)
            instance.user_permissions.add(delete_image_permission, delete_album_permission,)
        except ObjectDoesNotExist:
            # Permissions are not yet installed or conten does not created yet
            # probaly this is first
            pass


if SELF_MANAGE:
    post_save.connect(setup_imagestore_permissions, User)