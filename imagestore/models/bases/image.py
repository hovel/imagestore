# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import swapper
import logging
import logging.config
from django.conf import settings
from django.contrib.auth.models import Permission
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models import permalink
from django.db.models.signals import post_save
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from sorl.thumbnail import ImageField, get_thumbnail
from sorl.thumbnail.helpers import ThumbnailError
from tagging.fields import TagField
from imagestore.utils import FilePathGenerator

logger = logging.getLogger(__name__)

SELF_MANAGE = getattr(settings, 'IMAGESTORE_SELF_MANAGE', True)
UPLOAD_TO = getattr(settings, 'IMAGESTORE_UPLOAD_TO', 'imagestore/')


@python_2_unicode_compatible
class BaseImage(models.Model):
    title = models.CharField(verbose_name=_('Title'), max_length=255,
                             blank=True, null=True)
    description = models.TextField(verbose_name=_('Description'),
                                   blank=True, null=True)
    tags = TagField(verbose_name=_('Tags'), blank=True)
    order = models.IntegerField(verbose_name=_('Order'), default=0)
    image = ImageField(verbose_name=_('File'), max_length=255,
                       upload_to=FilePathGenerator(to=UPLOAD_TO))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             verbose_name=_('User'),
                             blank=True, null=True, related_name='images')
    created = models.DateTimeField(verbose_name=_('Created'), auto_now_add=True,
                                   null=True)
    updated = models.DateTimeField(verbose_name=_('Updated'), auto_now=True,
                                   null=True)
    album = models.ForeignKey(swapper.get_model_name('imagestore', 'Album'),
                              on_delete=models.CASCADE, verbose_name=_('Album'),
                              blank=True, null=True, related_name='images')

    class Meta:
        abstract = True
        ordering = ('order', 'id')
        permissions = (
            ('moderate_images', 'View, update and delete any image'),
        )

    def __str__(self):
        return '%s' % self.id

    @permalink
    def get_absolute_url(self):
        return 'imagestore:image', (), {'pk': self.id}

    def admin_thumbnail(self):
        try:
            thumb = get_thumbnail(self.image, '100x100', crop='center')
            return '<img src="{}" alt="">'.format(thumb.url)
        except (IOError, ThumbnailError):
            logger.info('Can\'t crate thumbnail from image {}'.format(self),
                        exc_info=settings.DEBUG)
            return ''

    admin_thumbnail.short_description = _('Thumbnail')
    admin_thumbnail.allow_tags = True


# noinspection PyUnusedLocal
def setup_imagestore_permissions(instance, created, **kwargs):
    if not created:
        return
    try:
        Album = swapper.load_model('imagestore', 'Album')
        Image = swapper.load_model('imagestore', 'Image')

        perms = []

        for model_class in [Album, Image]:
            for perm_name in ['add', 'change', 'delete']:
                app_label = model_class._meta.app_label
                model_name = model_class.__name__.lower()
                perm = Permission.objects.get_by_natural_key(
                    '{}_{}'.format(perm_name, model_name), app_label, model_name)
                perms.append(perm)

        instance.user_permissions.add(*perms)

    except ObjectDoesNotExist:
        # Permissions are not yet installed or content does not created yet
        # probaly this is first
        pass


if SELF_MANAGE:
    post_save.connect(setup_imagestore_permissions, settings.AUTH_USER_MODEL)
