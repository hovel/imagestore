#!/usr/bin/env python
# vim:fileencoding=utf-8

__author__ = 'zeus'
from django.conf import settings
from utils import get_model_string

def imagestore_processor(request):
    template = getattr(settings, 'IMAGESTORE_TEMPLATE', False)
    ret = {
        'IMAGESTORE_SHOW_USER': getattr(settings, 'IMAGESTORE_SHOW_USER', True),
        'IMAGESTORE_SHOW_TAGS': getattr(settings, 'IMAGESTORE_SHOW_TAGS', True),
        'IMAGESTORE_MODEL_STRING': get_model_string('Image')
        }
    if template:
        ret['IMAGESTORE_TEMPLATE'] = template
    return ret

  