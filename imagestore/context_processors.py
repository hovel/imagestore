#!/usr/bin/env python
# vim:fileencoding=utf-8

__author__ = 'zeus'
from django.conf import settings

def imagestore_processor(request):
    template = getattr(settings, 'IMAGESTORE_TEMPLATE', False)
    ret = {
        'IMAGESTORE_SHOW_USER': getattr(settings, 'IMAGESTORE_SHOW_USER', True),
        'IMAGESTORE_SHOW_TAGS': getattr(settings, 'IMAGESTORE_SHOW_TAGS', True)
        }
    if template:
        ret['IMAGESTORE_TEMPLATE'] = template
    return ret

  