# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import template
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.encoding import force_text
from django.utils.html import conditional_escape

register = template.Library()


@register.simple_tag
def imagestore_alt(image, counter=None):
    data = ''
    if image.title:
        data = image.title
    elif hasattr(image.album, 'brief'):
        if image.album.brief and counter is not None:
            try:
                tpl = force_text(getattr(
                    settings, 'IMAGESTORE_BRIEF_TO_ALT_TEMPLATE', '{0}_{1}'))
                data = tpl.format(image.album.brief, counter)
            except IndexError:
                raise ImproperlyConfigured('IMAGESTORE_BRIEF_TO_ALT_TEMPLATE '
                                           'has wrong format')
        elif image.album.brief:
            data = image.album.brief
    return 'alt="{}"'.format(conditional_escape(data))
