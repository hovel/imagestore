from imagestore.forms import ImageForm, AlbumForm
from imagestore.models import Album
from django import forms
from mezzanine import template
from django.forms.widgets import TextInput
from django.db.models import Min

register = template.Library()

@register.inclusion_tag("imagestore/forms/min_image_form.html", takes_context=True)
def render_minimal_image_upload_form(context, album_id):
    album = Album.objects.get(id=album_id)

    initial_data = {
                        "title"         : 'Untitled',
                        "description"   : '',
                        "album"         : album.name,
                        "tags"          : ''      
                    }
    form = ImageForm(context["request"].user, initial=initial_data)
    form.fields['album'].empty_label = None
    form.fields['album'].queryset = Album.objects.filter(id=album_id)
    form.fields['album'].initial = album.name

    form.fields['tagged_categories'].widget.attrs['style'] = 'display:none'
    form.fields['tagged_categories'].queryset = Album.objects.none()
    form.fields['tagged_categories'].label = ''
    form.fields['tagged_categories'].help_text = ''

    form.fields['title'].widget.attrs['style'] = 'display:none'
    form.fields['title'].label = ''

    form.fields['description'].widget.attrs['style'] = 'display:none'
    form.fields['description'].label = ''

    form.fields['album'].widget.attrs['style'] = 'display:none'
    form.fields['album'].label = ''

    form.fields['tags'].widget.attrs['style'] = 'display:none'
    form.fields['tags'].label = ''
    
    form.fields['image'].widget.attrs['style'] = 'display:none'
    form.fields['image'].label = ''

    context.update({
        "form": form,
    })
    return context

@register.inclusion_tag("imagestore/forms/min_album_form.html", takes_context=True)
def render_minimal_album_update_form(context, album_id):
    album = Album.objects.get(id=album_id)

    initial_data = {
                        "name"         : album.name,
                        "is_public"    : album.is_public,
                        "order"        : album.order      
                    }
    form = AlbumForm(initial=initial_data)
    form.fields['head'].widget.attrs['style'] = 'display:none'
    form.fields['head'].label = ''
    form.fields['order'].widget.attrs['style'] = 'display:none'
    form.fields['order'].label = ''

    context.update({
        "form": form,
        "album":album
    })
    return context

@register.filter
def min_image_order(album):
    if album:
        return album.images.all().aggregate(Min('order'))['order__min']
    return ''