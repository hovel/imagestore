# coding=utf-8
from __future__ import unicode_literals
from django.conf import settings


def get_user_model():
    try:
        from django.contrib.auth import get_user_model
        return get_user_model()
    except ImportError:
        from django.contrib.auth.models import User
        return User


def get_user_model_name():
    if hasattr(settings, 'AUTH_USER_MODEL'):
        return settings.AUTH_USER_MODEL
    else:
        return 'auth.User'