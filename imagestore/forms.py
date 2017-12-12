#!/usr/bin/env python
# vim:fileencoding=utf-8
from __future__ import unicode_literals
import swapper
from django import forms
try:
    from dal.autocomplete import FutureModelForm, TaggingSelect2
    AUTOCOMPLETE_LIGHT_INSTALLED = True
except ImportError:
    FutureModelForm = forms.ModelForm
    AUTOCOMPLETE_LIGHT_INSTALLED = False
from django.utils.translation import ugettext_lazy as _
Image = swapper.load_model('imagestore', 'Image')
Album = swapper.load_model('imagestore', 'Album')


class ImageForm(FutureModelForm):
    class Meta:
        model = Image
        exclude = ('user', 'order')

    description = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 2, 'cols': 19}), required=False,
        label=_('Description'))

    def __init__(self, user, *args, **kwargs):
        super(ImageForm, self).__init__(*args, **kwargs)
        self.fields['album'].queryset = Album.objects.filter(user=user)
        self.fields['album'].required = True
        if AUTOCOMPLETE_LIGHT_INSTALLED:
            self.fields['tags'].widget = TaggingSelect2(url='tag-autocomplete')


class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        exclude = ('user', 'created', 'updated')

    def __init__(self, *args, **kwargs):
        super(AlbumForm, self).__init__(*args, **kwargs)
        if 'instance' in kwargs and kwargs['instance']:
            self.fields['head'].queryset = Image.objects.filter(album=kwargs['instance'])
        else:
            self.fields['head'].widget = forms.HiddenInput()
