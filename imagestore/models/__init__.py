#!/usr/bin/env python
# vim:fileencoding=utf-8
from __future__ import unicode_literals
import django
from django.db import models
import swapper

if django.VERSION[:2] < (1, 5):
    if swapper.is_swapped('imagestore', 'Album'):
        app_name, model_name = swapper.get_model_name('imagestore', 'Album').split('.')
        Album = models.get_model(app_name, model_name)
    else:
        from .album import Album

    if swapper.is_swapped('imagestore', 'Image'):
        app_name, model_name = swapper.get_model_name('imagestore', 'Image').split('.')
        Image = models.get_model(app_name, model_name)
    else:
        from .image import Image
else:
    from .album import Album
    from .image import Image

from .upload import AlbumUpload
