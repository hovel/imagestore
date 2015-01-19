#!/usr/bin/env python
# vim:fileencoding=utf-8

from __future__ import unicode_literals
import os
import uuid
from django.core.exceptions import ImproperlyConfigured
from django.utils.importlib import import_module


def load_class(class_path, setting_name=None):
    """
    Loads a class given a class_path.
    The setting_name parameter is only there for pretty error output, and
    therefore is optional

    Taken from https://github.com/divio/django-shop/blob/master/shop/util/loader.py
    """
    try:
        class_module, class_name = class_path.rsplit('.', 1)
    except ValueError:
        if setting_name:
            txt = '%s isn\'t a valid module. Check your %s setting' % (class_path,setting_name)
        else:
            txt = '%s isn\'t a valid module.' % class_path
        raise ImproperlyConfigured(txt)

    try:
        mod = import_module(class_module)
    except ImportError as e:
        if setting_name:
            txt = 'Error importing backend %s: "%s". Check your %s setting' % (class_module, e, setting_name)
        else:
            txt = 'Error importing backend %s: "%s".' % (class_module, e)
        raise ImproperlyConfigured(txt)

    try:
        clazz = getattr(mod, class_name)
    except AttributeError as e:
        if setting_name:
            txt = 'Backend module "%s" does not define a "%s" class. Check your %s setting. (%s)' % (class_module, class_name, setting_name)
        else:
            txt = 'Backend module "%s" does not define a "%s" class. (%s)' % (class_module, class_name, e)
        raise ImproperlyConfigured(txt)
    return clazz


class FilePathGenerator(object):
    """
    Special class for generating random filenames
    Can be deconstructed for correct migration
    """

    def __init__(self, to, *args, **kwargs):
        self.to = to

    def deconstruct(self, *args, **kwargs):
        return 'imagestore.utils.FilePathGenerator', [], {'to': self.to}

    def __call__(self, instance, filename):
        """
        This function generate filename with uuid4
        it's useful if:
        - you don't want to allow others to see original uploaded filenames
        - users can upload images with unicode in filenames wich can confuse browsers and filesystem
        """
        ext = filename.split('.')[-1]
        filename = "%s.%s" % (uuid.uuid4(), ext)
        return os.path.join(self.to, filename)
