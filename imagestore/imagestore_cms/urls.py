#!/usr/bin/env python
# vim:fileencoding=utf-8
from __future__ import unicode_literals
from django.conf.urls import url, include


urlpatterns = [
    url(r'^', include('imagestore.urls', namespace='imagestore')),
]
