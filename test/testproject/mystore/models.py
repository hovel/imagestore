# coding=utf-8
from __future__ import unicode_literals
from django.db import models
from imagestore.models.bases.image import BaseImage


class MyImage(BaseImage):
    some_int = models.IntegerField()