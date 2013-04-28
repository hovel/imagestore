#!/usr/bin/env python
# vim:fileencoding=utf-8

__author__ = 'zeus'

import os
import uuid
from django.core.exceptions import ImproperlyConfigured
from django.utils.importlib import import_module
from django.conf import settings

UPLOAD_TO = getattr(settings, 'IMAGESTORE_UPLOAD_TO', 'imagestore/')

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
    except ImportError, e:
        if setting_name:
            txt = 'Error importing backend %s: "%s". Check your %s setting' % (class_module, e, setting_name)
        else:
            txt = 'Error importing backend %s: "%s".' % (class_module, e)
        raise ImproperlyConfigured(txt)

    try:
        clazz = getattr(mod, class_name)
    except AttributeError, e:
        if setting_name:
            txt = 'Backend module "%s" does not define a "%s" class. Check your %s setting. (%s)' % (class_module, class_name, setting_name)
        else:
            txt = 'Backend module "%s" does not define a "%s" class. (%s)' % (class_module, class_name, e)
        raise ImproperlyConfigured(txt)
    return clazz

def get_model_string(model_name):
    """
    Returns the model string notation Django uses for lazily loaded ForeignKeys
    (eg 'auth.User') to prevent circular imports.
    This is needed to allow our crazy custom model usage.

    Taken from https://github.com/divio/django-shop/blob/master/shop/util/loader.py
    """
    class_path = getattr(settings, 'IMAGESTORE_%s_MODEL' % model_name.upper().replace('_', ''), None)
    if not class_path:
        return 'imagestore.%s' % model_name
    else:
        klass = load_class(class_path)
        return '%s.%s' % (klass._meta.app_label, klass.__name__)

def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join(UPLOAD_TO, filename)