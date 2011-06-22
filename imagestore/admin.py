from django.contrib import admin
from imagestore.models import Image, Album, AlbumUpload
from sorl.thumbnail.admin import AdminImageMixin

try:
    from places.models import GeoPlace
except:
    GeoPlace = None

class AlbumAdmin(admin.ModelAdmin):
    fieldsets = ((None, {'fields': ['name', 'user', 'is_public']}),)
    list_display = ('name', 'admin_thumbnail','user', 'created', 'updated', 'is_public')

admin.site.register(Album, AlbumAdmin)

class ImageAdmin(admin.ModelAdmin):
    fieldsets = ((None, {'fields': ['user', 'title', 'image', 'description', 'order', 'tags', 'album']}),)
    list_display = ('admin_thumbnail', 'user', 'order', 'album', 'title')
    raw_id_fields = ('user', )

class AlbumUploadAdmin(admin.ModelAdmin):
    def has_change_permission(self, request, obj=None):
        return False

if GeoPlace:
    ImageAdmin.fieldsets[0][1]['fields'].append('place')
    ImageAdmin.raw_id_fields = ('place',)

admin.site.register(Image, ImageAdmin)
admin.site.register(AlbumUpload, AlbumUploadAdmin)
