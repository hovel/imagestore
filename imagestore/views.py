from django.http import HttpResponseForbidden
from imagestore.models import Image, Category
from django.shortcuts import get_object_or_404
from django.views.generic.list_detail import object_list
from django.conf import settings
from annoying.decorators import render_to


IMAGESTORE_ON_PAGE = getattr(settings, 'IMAGESTORE_ON_PAGE', 12)

def filter_access(request, category=None):
    '''
    Filter images that current user can access
    '''
    filter = {}
    if not request.user.is_staff:
        filter['is_public'] = True
    return filter

def category(request, slug, *args, **kwargs):
    '''
    Category view
    Filter images for current user access
    '''
    category = get_object_or_404(Category, slug=slug)
    if not (request.user.is_staff or category.is_public):
        return HttpResponseForbidden()
    filter = filter_access(request)
    kwargs['queryset'] = Image.objects.filter(**filter).filter(category=category).order_by('order', 'id')
    kwargs['template_object_name'] = 'images'
    kwargs['template_name'] = 'imagestore/category.html'
    kwargs['extra_context'] = {'category': category}
    return object_list(request, *args, **kwargs)

@render_to('imagestore/gallery.html')
def category_list(request):
    categories = Category.objects.order_by('order')
    if not request.user.is_staff:
        categories = categories.filter(is_public__exact=True, parent_category=None)
    return {'categories_list': categories}
