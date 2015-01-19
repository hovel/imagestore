#!/usr/bin/env python
# vim:fileencoding=utf-8
from __future__ import unicode_literals
import swapper
import django
from django.utils.translation import ugettext_lazy as _
from .bases.image import BaseImage


if django.VERSION[:2] < (1, 5):
    class ImageMeta(BaseImage.Meta):
        abstract = False
        app_label = 'imagestore'
        verbose_name = _('Image')
        verbose_name_plural = _('Images')
else:
    class ImageMeta(BaseImage.Meta):
        abstract = False
        app_label = 'imagestore'
        verbose_name = _('Image')
        verbose_name_plural = _('Images')
        swappable = swapper.swappable_setting('imagestore', 'Image')


class Image(BaseImage):
    Meta = ImageMeta
