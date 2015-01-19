#!/usr/bin/env python
# vim:fileencoding=utf-8
from __future__ import unicode_literals
try:
    from django.conf.urls import patterns, url, include
except ImportError:
    from django.conf.urls.defaults import patterns, url, include


urlpatterns = patterns(
    '',
    url(r'^', include('imagestore.urls', namespace='imagestore')),
)
