#!/usr/bin/env python
# vim:fileencoding=utf-8

__author__ = 'zeus'

try:
    from django.conf.urls import patterns, url, include
except ImportError:
    from django.conf.urls.defaults import patterns, url, include

from imagestore.views import AlbumListView

urlpatterns = patterns('',
    url(r'^', include('imagestore.urls', namespace='imagestore')),
    )
