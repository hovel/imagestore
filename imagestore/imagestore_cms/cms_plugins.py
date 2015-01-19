#!/usr/bin/env python
# vim:fileencoding=utf-8
from __future__ import unicode_literals
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from .models import ImagestoreAlbumPtr, ImagestoreAlbumCarousel
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

class AlbumPlugin(CMSPluginBase):
    model = ImagestoreAlbumPtr
    name = _('Album')
    render_template = "cms/plugins/imagestore_album.html"
    text_enabled = True

    def render(self, context, instance, placeholder):
        context.update({'album': instance.album})
        return context


class AlbumCarouselPlugin(CMSPluginBase):
    model = ImagestoreAlbumCarousel
    name = _('Album as carousel')
    render_template = "cms/plugins/imagestore_album_carousel.html"
    text_enabled = True

    def render(self, context, instance, placeholder):

        # default carousel template in the settings file
        carousel_template = getattr(settings, 'IMAGESTORE_CAROUSEL_TEMPLATE', None)
        
        if carousel_template:
            self.render_template = carousel_template

        if instance.template_file:
            self.render_template = instance.template_file
        else:
            if carousel_template:
                instance.template_file = carousel_template
            else:
                instance.template_file = self.render_template
                instance.save()

        images = instance.album.images.all()
        if instance.limit:
            images = images[:instance.limit]
        context.update({'images': images, 'carousel': instance})
        return context

plugin_pool.register_plugin(AlbumCarouselPlugin)
plugin_pool.register_plugin(AlbumPlugin)