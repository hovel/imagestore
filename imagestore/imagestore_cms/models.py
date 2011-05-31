#!/usr/bin/env python
# vim:fileencoding=utf-8

__author__ = 'zeus'

from cms.models import CMSPlugin
from django.db import models
from imagestore.models import Album
from django.utils.translation import ugettext_lazy as _

class ImagestoreAlbumPtr(CMSPlugin):
    album = models.ForeignKey(Album, verbose_name=_('Album'), blank=False, null=False)

class ImagestoreAlbumCarousel(CMSPlugin):
    album = models.ForeignKey(Album, verbose_name=_('Album'), blank=False, null=False)
    skin = models.CharField(max_length=100, verbose_name=_('Skin'), default='jcarousel-skin-tango')
    limit = models.IntegerField(verbose_name=_('Image limit'), blank=True, null=True)
