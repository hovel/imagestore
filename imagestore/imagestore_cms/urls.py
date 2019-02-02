#!/usr/bin/env python
# vim:fileencoding=utf-8
from __future__ import unicode_literals
from django.conf.urls import url, include

app_name = 'imagestore_cms'

urlpatterns = [
    url(r'^', include('imagestore.urls', namespace='imagestore')),
]
