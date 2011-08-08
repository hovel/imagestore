#!/usr/bin/env python
# vim:fileencoding=utf-8

__author__ = 'zeus'

from bases.album import BaseAlbum
from django.utils.translation import ugettext_lazy as _
from imagestore.utils import load_class, get_model_string

class Album(BaseAlbum):

    class Meta(BaseAlbum.Meta):
        abstract = False
        verbose_name = _('Album')
        verbose_name_plural = _('Albums')
        app_label = 'imagestore'