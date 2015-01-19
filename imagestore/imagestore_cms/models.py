#!/usr/bin/env python
# vim:fileencoding=utf-8
from __future__ import unicode_literals
from cms.models import CMSPlugin
from django.db import models
import swapper
from django.utils.translation import ugettext_lazy as _
from django.conf import settings


class ImagestoreAlbumPtr(CMSPlugin):
    album = models.ForeignKey(swapper.get_model_name('imagestore', 'Album'), verbose_name=_('Album'),
                              blank=False, null=False)


class ImagestoreAlbumCarousel(CMSPlugin):
    album = models.ForeignKey(swapper.get_model_name('imagestore', 'Album'), verbose_name=_('Album'),
                              blank=False, null=False)
    skin = models.CharField(max_length=100, verbose_name=_('Skin'), default='jcarousel-skin-tango')
    limit = models.IntegerField(verbose_name=_('Image limit'), blank=True, null=True)
    size = models.CharField(max_length=20, verbose_name=_('Thumbnail size'), default='72x72')
    full_size = models.CharField(max_length=20, verbose_name=_('Full size view'), default='600x600')
    template_file = models.CharField(max_length=100, verbose_name=_('Template file'),
                                     default=getattr(settings, 'IMAGESTORE_CAROUSEL_TEMPLATE',
                                                     'cms/plugins/imagestore_album_carousel.html'),
                                     blank=True, null=True)