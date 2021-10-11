# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils.translation import gettext_lazy as _

from imagestore.models.bases.album import BaseAlbum
from imagestore.models.bases.image import BaseImage


class MyAlbum(BaseAlbum):

    class Meta(BaseAlbum.Meta):
        app_label = 'mystore'
        verbose_name = _('Album')
        verbose_name_plural = _('Album')


class MyImage(BaseImage):
    some_int = models.IntegerField()

    class Meta(BaseImage.Meta):
        app_label = 'mystore'
        verbose_name = _('Image')
        verbose_name_plural = _('Images')
