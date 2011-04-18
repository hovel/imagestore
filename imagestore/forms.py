#!/usr/bin/env python
# vim:fileencoding=utf-8

__author__ = 'zeus'

from django import forms
from models import Image, Album
from django.utils.translation import ugettext_lazy as _

try:
    from places.models import GeoPlace
except:
    GeoPlace = None

class ImageForm(forms.ModelForm):
    class Meta(object):
        model = Image
        exclude = ('user', 'order')

    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 2, 'cols': 19}), required=False,
                                  label=_('Description'))

    def __init__(self, user, *args, **kwargs):
        super(ImageForm, self).__init__(*args, **kwargs)
        self.fields['album'].queryset = Album.objects.filter(user=user)
        self.fields['album'].required = True

        if GeoPlace:
            self.fields['place'] = forms.CharField(required=False, label=_('Place'), widget=forms.HiddenInput)
            self.fields['place_text'] = forms.CharField(required=False, label=_('Place'))

            if 'instance' in kwargs and kwargs['instance'] and kwargs['instance'].place:
                self.fields['place_text'].initial = kwargs['instance'].place.name

    def clean_place_text(self):
        name = self.data.get('place_text', None)
        if not name:
            return None
        try:
            place = GeoPlace.objects.get(name=name)
        except:
            raise forms.ValidationError(_("Place doesn't found"))
        return place

    def clean_place(self):
        return self.clean_place_text()


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
