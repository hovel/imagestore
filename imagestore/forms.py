#!/usr/bin/env python
# vim:fileencoding=utf-8
import inspect

__author__ = 'zeus'

from django import forms
from models import Image

class ImageForm(forms.ModelForm):
    class Meta(object):
        model = Image
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        if args:
            kwargs.update(dict(zip(inspect.getargspec(super(ImageForm, self).__init__)[0][1:], args)))
        super(ImageForm, self).__init__(**kwargs)
        if 'instance' in kwargs:
            self.fields['image'].required = False