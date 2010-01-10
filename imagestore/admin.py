from django.contrib import admin
from django.utils.translation import ugettext as _
from imagestore.models import Image, Category

class CategoryAdmin(admin.ModelAdmin):
    fieldsets = ((None, {'fields': ['slug', 'title', 'order', 'parent_category', 'is_public']}),)
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'slug', 'order', 'is_public')

admin.site.register(Category, CategoryAdmin)

class ImageAdmin(admin.ModelAdmin):
    fieldsets = ((None, {'fields': ['title', 'slug', 'image', 'description', 'order', 'tags', 'category', 'is_public']}),)
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('id', 'order', 'category', 'title', 'slug', 'tags', 'is_public')

admin.site.register(Image, ImageAdmin)
