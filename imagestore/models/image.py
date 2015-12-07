# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import swapper
from django.utils.translation import ugettext_lazy as _
from .bases.image import BaseImage


class Image(BaseImage):
    class Meta(BaseImage.Meta):
        abstract = False
        app_label = 'imagestore'
        verbose_name = _('Image')
        verbose_name_plural = _('Images')
        swappable = swapper.swappable_setting('imagestore', 'Image')
