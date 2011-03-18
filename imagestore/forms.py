#!/usr/bin/env python
# vim:fileencoding=utf-8
import inspect

__author__ = 'zeus'

from django import forms
from models import Image, Album

class ImageForm(forms.ModelForm):

    def __init__(self, user, *args, **kwargs):
        super(ImageForm, self).__init__(*args, **kwargs)
        self.fields['album'].queryset = Album.objects.filter(user=user)
        self.fields['album'].required = True

    class Meta(object):
        model = Image
        exclude = ('user', 'order')

    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 2, 'cols': 19}), required=False)

#    def __init__(self, *args, **kwargs):
#        if args:
#            kwargs.update(dict(zip(inspect.getargspec(super(ImageForm, self).__init__)[0][1:], args)))
#        super(ImageForm, self).__init__(**kwargs)
#        if 'instance' in kwargs:
#            self.fields['image'].required = False


class AlbumForm(forms.ModelForm):
    class Meta(object):
        model = Album
        exclude = ('user', 'created', 'updated')

    def __init__(self, *args, **kwargs):
        super(AlbumForm, self).__init__(*args, **kwargs)
        if 'instance' in kwargs and kwargs['instance']:
            self.fields['head'].queryset = Image.objects.filter(album=kwargs['instance'])
        else:
            self.fields['head'].widget = forms.HiddenInput()
