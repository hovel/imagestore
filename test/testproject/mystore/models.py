# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils.translation import ugettext_lazy as _
from imagestore.models.bases.image import BaseImage


class MyImage(BaseImage):
    some_int = models.IntegerField()

    class Meta(BaseImage.Meta):
        verbose_name = _('Image')
        verbose_name_plural = _('Images')
