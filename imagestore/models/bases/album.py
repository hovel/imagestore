# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging
import logging.config
import swapper
from django.conf import settings
from django.db import models
from django.db.models import permalink
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from sorl.thumbnail import get_thumbnail
from sorl.thumbnail.helpers import ThumbnailError

logger = logging.getLogger(__name__)

SELF_MANAGE = getattr(settings, 'IMAGESTORE_SELF_MANAGE', True)


@python_2_unicode_compatible
class BaseAlbum(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, verbose_name=_('User'),
                             blank=True, null=True, related_name='albums')
    name = models.CharField(verbose_name=_('Name'), max_length=100,
                            blank=False, null=False)
    brief = models.CharField(verbose_name=_('Brief'), max_length=255,
                             blank=True, default='',
                             help_text=_('Short description'))
    created = models.DateTimeField(verbose_name=_('Created'), auto_now_add=True)
    updated = models.DateTimeField(verbose_name=_('Updated'), auto_now=True)
    is_public = models.BooleanField(verbose_name=_('Is public'), default=True)
    head = models.ForeignKey(swapper.get_model_name('imagestore', 'Image'),
                             on_delete=models.SET_NULL, verbose_name=_('Head'),
                             related_name='head_of', blank=True, null=True)
    order = models.IntegerField(verbose_name=_('Order'), default=0)

    class Meta:
        abstract = True
        ordering = ('order', 'created', 'name')
        permissions = (
            ('moderate_albums', 'View, update and delete any album'),
        )

    def __str__(self):
        return self.name

    @permalink
    def get_absolute_url(self):
        return 'imagestore:album', (), {'album_id': self.id}

    def admin_thumbnail(self):
        img = self.get_head()
        if not img:
            return _('Empty album')

        try:
            thumb = get_thumbnail(img.image, '100x100', crop='center')
            return '<img src="{}" alt="">'.format(thumb.url)
        except (IOError, ThumbnailError):
            logger.info('Can\'t crate thumbnail from image {}'.format(img),
                        exc_info=settings.DEBUG)
            return ''

    def get_head(self):
        if not self.head:
            self.head = self.images.first()
            if self.head:
                self.save()
        return self.head

    admin_thumbnail.short_description = _('Head')
    admin_thumbnail.allow_tags = True
