# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import swapper
from django.utils.translation import ugettext_lazy as _
from .bases.album import BaseAlbum


class Album(BaseAlbum):
    class Meta(BaseAlbum.Meta):
        abstract = False
        app_label = 'imagestore'
        verbose_name = _('Album')
        verbose_name_plural = _('Albums')
        swappable = swapper.swappable_setting('imagestore', 'Album')
