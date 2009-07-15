from django.contrib import admin
from django.utils.translation import ugettext as _
from imagestore.models import Image, Category

class CategoryAdmin(admin.ModelAdmin):
    fieldsets = ((None, {'fields': ['slug', 'title', 'order']}),)
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'slug', 'order')

admin.site.register(Category, CategoryAdmin)

class ImageAdmin(admin.ModelAdmin):
    fieldsets = ((None, {'fields': ['title', 'slug', 'image', 'author', 'description', 'order', 'tags', 'category']}),)
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('id', 'order', 'title', 'slug', 'author', 'tags')

admin.site.register(Image, ImageAdmin)
