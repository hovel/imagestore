#!/usr/bin/env python
# vim:fileencoding=utf-8

__author__ = 'zeus'
from django.conf import settings

def imagestore_processor(request):
    template = getattr(settings, 'IMAGESTORE_TEMPLATE', False)
    imagestore_show_user = getattr(settings, 'IMAGESTORE_SHOW_USER', True)
    ret = {'IMAGESTORE_SHOW_USER': imagestore_show_user,}
    if template:
        ret['IMAGESTORE_TEMPLATE'] = template,
    return ret

  