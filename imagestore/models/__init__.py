#!/usr/bin/env python
# vim:fileencoding=utf-8

__author__ = 'zeus'
from imagestore.utils import load_class, get_model_string
from django.conf import settings

Album = load_class(getattr(settings, 'IMAGESTORE_ALBUM_MODEL', 'imagestore.models.album.Album'))
Image = load_class(getattr(settings, 'IMAGESTORE_IMAGE_MODEL', 'imagestore.models.image.Image'))
from upload import AlbumUpload