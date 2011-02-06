#!/usr/bin/env python
# vim:fileencoding=utf-8

__author__ = 'zeus'
from django.conf import settings

def imagestore_processor(request):
    template = getattr(settings, 'IMAGESTORE_TEMPLATE', False)
    if template:
        return {'IMAGESTORE_TEMPLATE': template}
    else:
        return {}

  