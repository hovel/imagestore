from __future__ import unicode_literals
from django.contrib import admin
import swapper
from imagestore.models.album import Album
from imagestore.models.image import Image
from imagestore.models.upload import AlbumUpload
from sorl.thumbnail.admin import AdminInlineImageMixin


class InlineImageAdmin(AdminInlineImageMixin, admin.TabularInline):
    model = Image
    fieldsets = ((None, {'fields': ['image', 'user', 'title', 'order', 'tags', 'album']}),)
    raw_id_fields = ('user', )
    extra = 0


class AlbumAdmin(admin.ModelAdmin):
    fieldsets = ((None, {'fields': ['name', 'brief', 'user', 'is_public', 'order']}),)
    list_display = ('name', 'admin_thumbnail', 'user', 'created', 'updated', 'is_public', 'order')
    list_editable = ('order', )
    inlines = [InlineImageAdmin]


class ImageAdmin(admin.ModelAdmin):
    fieldsets = ((None, {'fields': ['user', 'title', 'image', 'description', 'order', 'tags', 'album']}),)
    list_display = ('admin_thumbnail', 'user', 'order', 'album', 'title')
    raw_id_fields = ('user', )
    list_filter = ('album', )


class AlbumUploadAdmin(admin.ModelAdmin):
    def has_change_permission(self, request, obj=None):
        return False

if not swapper.is_swapped('imagestore', 'Image'):
    admin.site.register(Image, ImageAdmin)

if not swapper.is_swapped('imagestore', 'Album'):
    admin.site.register(Album, AlbumAdmin)
    admin.site.register(AlbumUpload, AlbumUploadAdmin)
