#!/usr/bin/env python
# vim:fileencoding=utf-8
from __future__ import unicode_literals
import swapper
import django
from django.utils.translation import ugettext_lazy as _
from .bases.album import BaseAlbum


if django.VERSION[:2] < (1, 5):
    class AlbumMeta(BaseAlbum.Meta):
        abstract = False
        app_label = 'imagestore'
        verbose_name = _('Album')
        verbose_name_plural = _('Albums')
else:
    class AlbumMeta(BaseAlbum.Meta):
        abstract = False
        app_label = 'imagestore'
        verbose_name = _('Album')
        verbose_name_plural = _('Albums')
        swappable = swapper.swappable_setting('imagestore', 'Album')


class Album(BaseAlbum):
    Meta = AlbumMeta
