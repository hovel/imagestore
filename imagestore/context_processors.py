#!/usr/bin/env python
# vim:fileencoding=utf-8
from __future__ import unicode_literals
from django.core.urlresolvers import reverse, NoReverseMatch
from django.conf import settings
import swapper

Image = swapper.load_model('imagestore', 'Image')
Album = swapper.load_model('imagestore', 'Album')


def imagestore_processor(request):
    template = getattr(settings, 'IMAGESTORE_TEMPLATE', False)
    ret = {
        'IMAGESTORE_SHOW_USER': getattr(settings, 'IMAGESTORE_SHOW_USER', True),
        'IMAGESTORE_SHOW_TAGS': getattr(settings, 'IMAGESTORE_SHOW_TAGS',
                                        not swapper.is_swapped('imagestore', 'Image')),
        'IMAGESTORE_LOAD_CSS': getattr(settings, 'IMAGESTORE_LOAD_CSS', True)
    }
    try:
        ret['imagestore_index_url'] = reverse('imagestore:index')
    except NoReverseMatch:  # Bastard django-cms from hell!!!!111
        pass
    if template:
        ret['IMAGESTORE_TEMPLATE'] = template
    image_applabel, image_classname = Image._meta.app_label, Image.__name__.lower()
    album_applabel, album_classname = Album._meta.app_label, Album.__name__.lower()
    ret['imagestore_perms'] = {
        'add_image': request.user.has_perm('%s.add_%s' % (image_applabel, image_classname)),
        'add_album': request.user.has_perm('%s.add_%s' % (album_applabel, album_classname)),
    }
    return ret

  