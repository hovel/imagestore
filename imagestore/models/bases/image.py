# coding=utf-8
from __future__ import unicode_literals
import django
from django.db import models
from django.db.models import permalink
from django.utils.encoding import python_2_unicode_compatible
from sorl.thumbnail.helpers import ThumbnailError
import swapper
from tagging.fields import TagField
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from sorl.thumbnail import ImageField, get_thumbnail
from django.contrib.auth.models import Permission
from django.db.models.signals import post_save
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
import logging

logger = logging.getLogger(__name__)

from imagestore.utils import FilePathGenerator
from imagestore.compat import get_user_model_name, get_user_model

SELF_MANAGE = getattr(settings, 'IMAGESTORE_SELF_MANAGE', True)
UPLOAD_TO = getattr(settings, 'IMAGESTORE_UPLOAD_TO', 'imagestore/')

@python_2_unicode_compatible
class BaseImage(models.Model):
    class Meta(object):
        abstract = True
        ordering = ('order', 'id')
        permissions = (
            ('moderate_images', 'View, update and delete any image'),
        )

    title = models.CharField(_('Title'), max_length=255, blank=True, null=True)
    description = models.TextField(_('Description'), blank=True, null=True)
    tags = TagField(_('Tags'), blank=True)
    order = models.IntegerField(_('Order'), default=0)
    image = ImageField(verbose_name=_('File'), max_length=255, upload_to=FilePathGenerator(to=UPLOAD_TO))
    user = models.ForeignKey(get_user_model_name(), verbose_name=_('User'), null=True, blank=True, related_name='images')
    created = models.DateTimeField(_('Created'), auto_now_add=True, null=True)
    updated = models.DateTimeField(_('Updated'), auto_now=True, null=True)
    album = models.ForeignKey(swapper.get_model_name('imagestore', 'Album'), verbose_name=_('Album'),
                              null=True, blank=True, related_name='images')

    @permalink
    def get_absolute_url(self):
        return 'imagestore:image', (), {'pk': self.id}

    def __str__(self):
        return '%s' % self.id

    def admin_thumbnail(self):
        try:
            return '<img src="%s">' % get_thumbnail(self.image, '100x100', crop='center').url
        except IOError:
            logger.exception('IOError for image %s', self.image)
            return 'IOError'
        except ThumbnailError as ex:
            return 'ThumbnailError, %s' % ex.message

    admin_thumbnail.short_description = _('Thumbnail')
    admin_thumbnail.allow_tags = True


#noinspection PyUnusedLocal
def setup_imagestore_permissions(instance, created, **kwargs):
    if not created:
        return
    try:
        Album = swapper.load_model('imagestore', 'Album')
        Image = swapper.load_model('imagestore', 'Image')

        perms = []

        for model_class in [Album, Image]:
            for perm_name in ['add', 'change', 'delete']:
                app_label, model_name = model_class._meta.app_label, model_class.__name__.lower()
                perm = Permission.objects.get_by_natural_key('%s_%s' % (perm_name, model_name), app_label, model_name)
                perms.append(perm)

        instance.user_permissions.add(*perms)

    except ObjectDoesNotExist:
        # Permissions are not yet installed or content does not created yet
        # probaly this is first
        pass


if SELF_MANAGE:
    if django.VERSION[:2] >= (1, 7):
        post_save.connect(setup_imagestore_permissions, get_user_model_name())
    else:
        post_save.connect(setup_imagestore_permissions, get_user_model())
