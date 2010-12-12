from django.contrib import admin
from imagestore.models import Image, Category
from mptt.admin import MPTTModelAdmin

class CategoryAdmin(MPTTModelAdmin):
    fieldsets = ((None, {'fields': ['slug', 'title', 'order', 'parent', 'is_public']}),)
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'slug', 'order', 'is_public')

admin.site.register(Category, CategoryAdmin)

class ImageAdmin(admin.ModelAdmin):
    fieldsets = ((None, {'fields': ['user', 'title', 'image', 'description', 'order', 'tags', 'category', 'is_public']}),)
    list_display = ('id', 'user', 'order', 'category', 'title', 'is_public')
    list_filter = ('category', 'tags')
    raw_id_fields = ('user', )

admin.site.register(Image, ImageAdmin)
