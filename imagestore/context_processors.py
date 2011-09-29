#!/usr/bin/env python
# vim:fileencoding=utf-8

__author__ = 'zeus'
from django.conf import settings
from utils import get_model_string
from imagestore.models import Album, Image
from imagestore.models import image_applabel, image_classname
from imagestore.models import album_applabel, album_classname

def imagestore_processor(request):
    template = getattr(settings, 'IMAGESTORE_TEMPLATE', False)
    ret = {
        'IMAGESTORE_SHOW_USER': getattr(settings, 'IMAGESTORE_SHOW_USER', True),
        'IMAGESTORE_SHOW_TAGS': getattr(settings, 'IMAGESTORE_SHOW_TAGS', True),
        'IMAGESTORE_MODEL_STRING': get_model_string('Image')
        }
    if template:
        ret['IMAGESTORE_TEMPLATE'] = template
    ret['imagestore_perms'] = {
        'add_image': request.user.has_perm('%s.add_%s' % (image_applabel, image_classname)),
        'add_album': request.user.has_perm('%s.add_%s' % (album_applabel, album_classname)),
    }
    return ret

  