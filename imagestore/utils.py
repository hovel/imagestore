# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import uuid
import logging
import logging.config
from importlib import import_module
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.deconstruct import deconstructible
from django.utils.encoding import force_text

logger = logging.getLogger(__name__)


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
            txt = '%s isn\'t a valid module. Check your %s setting' % (class_path, setting_name)
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
            txt = 'Backend module "%s" does not define a "%s" class. Check your %s setting. (%s)' % (class_module, class_name, setting_name, e)
        else:
            txt = 'Backend module "%s" does not define a "%s" class. (%s)' % (class_module, class_name, e)
        raise ImproperlyConfigured(txt)
    return clazz


@deconstructible
class FilePathGenerator(object):
    """
    Special class for generating random filenames with `uuid.uuid4()`.
    Can be deconstructed for correct migration.
    It's useful if:
    - you don't want to allow others to see original names of uploaded files
    - you're afraid that weird unicode names can confuse browsers or filesystem
    """

    def __init__(self, to):
        self.to = to

    def __call__(self, instance, filename):
        extension = os.path.splitext(filename)[1]
        uuid_filename = force_text(uuid.uuid4()) + extension
        path = os.path.join(
            self.to, uuid_filename[:2], uuid_filename[2:4], uuid_filename)
        return path
