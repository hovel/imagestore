#!/usr/bin/env python
# vim:fileencoding=utf-8

__author__ = 'zeus'

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from models import ImagestoreAlbumPtr, ImagestoreAlbumCarousel
from django.utils.translation import ugettext_lazy as _

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
        images = instance.album.images.all()
        if instance.limit:
            images = images[:instance.limit]
        context.update({'images': images, 'carousel': instance, 'template': instance.template_file})
        return context

plugin_pool.register_plugin(AlbumCarouselPlugin)
plugin_pool.register_plugin(AlbumPlugin)