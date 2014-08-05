# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import template
from django.conf import settings
from django.utils.encoding import force_text

register = template.Library()


@register.simple_tag
def imagestore_alt(image, counter=None):
    data = ''
    if image.title:
        data = image.title
    elif hasattr(image.album, 'brief'):
        if image.album.brief and counter is not None:
            tpl = force_text(
                getattr(settings, 'IMAGESTORE_BRIEF_TO_ALT_TEMPLATE', '{0}_{1}')
            )
            try:
                if '{' not in tpl:
                    raise ValueError
                data = tpl.format(image.album.brief, counter)
            except (ValueError, IndexError):
                message = 'IMAGESTORE_BRIEF_TO_ALT_TEMPLATE has wrong format'
                print(message)
                if settings.DEBUG:
                    data = message
        elif image.album.brief:
            data = image.album.brief

    if data:
        data = data.replace('\'', '&#39;').replace('\"', '&#34;')
        return 'alt="{0}"'.format(data)
    else:
        return ''
