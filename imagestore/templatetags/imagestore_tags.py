# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import template
from django.conf import settings

register = template.Library()

@register.simple_tag
def imagestore_alt(image, counter=None):
    data = ''
    if image.title:
        data = image.title
    elif hasattr(image.album, 'brief'):
        if image.album.brief and counter is not None:
            tpl = unicode(getattr(settings, 'BRIEF_TO_ALT_WITH_COUNTER', '{0}_{1}'))
            data = tpl.format(image.album.brief, counter)
        elif image.album.brief:
            data = image.album.brief

    if data:
        return 'alt="{0}"'.format(data)
    else:
        return ''
