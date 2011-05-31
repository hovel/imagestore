#!/usr/bin/env python
# vim:fileencoding=utf-8

__author__ = 'zeus'

from django.conf.urls.defaults import *
from imagestore.views import AlbumListView

urlpatterns = patterns('',
    url(r'^', include('imagestore.urls', namespace='imagestore')),
    )