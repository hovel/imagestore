from django.contrib import admin
from django.utils.translation import ugettext as _
from imagestore.models import Image, Category

class CategoryAdmin(admin.ModelAdmin):
    fieldsets = ((None, {'fields': ['slug', 'title']}),)
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title',)

admin.site.register(Category, CategoryAdmin)

class ImageAdmin(admin.ModelAdmin):
    fieldsets = ((None, {'fields': ['title', 'slug', 'image', 'author', 'description', 'tags', 'category']}),)
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('id', 'title', 'slug', 'author', 'tags')

admin.site.register(Image, ImageAdmin)
