import swapper
from django.contrib import admin
from sorl.thumbnail.admin import AdminInlineImageMixin

Image = swapper.load_model('imagestore', 'Image')
Album = swapper.load_model('imagestore', 'Album')


class InlineImageAdmin(AdminInlineImageMixin, admin.TabularInline):
    model = Image
    extra = 0


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    inlines = [InlineImageAdmin]


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    pass
