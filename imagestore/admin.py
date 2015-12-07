from __future__ import unicode_literals
import swapper
from django.contrib import admin
from sorl.thumbnail.admin import AdminInlineImageMixin
from .models.album import Album
from .models.image import Image
from .models.upload import AlbumUpload


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
    list_display = ('admin_thumbnail', 'user', 'order', 'album', 'title', 'width', 'height')
    raw_id_fields = ('user', )
    list_filter = ('album', )

    def width(self, obj):
        try:
            return obj.image.width
        except IOError:
            return None

    def height(self, obj):
        try:
            return obj.image.height
        except IOError:
            return None


class AlbumUploadAdmin(admin.ModelAdmin):
    def has_change_permission(self, request, obj=None):
        return False

if not swapper.is_swapped('imagestore', 'Image'):
    admin.site.register(Image, ImageAdmin)

if not swapper.is_swapped('imagestore', 'Album'):
    admin.site.register(Album, AlbumAdmin)
    admin.site.register(AlbumUpload, AlbumUploadAdmin)
