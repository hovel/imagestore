from django.http import HttpResponseForbidden
from imagestore.models import Category, Image
from django.shortcuts import get_object_or_404
from django.views.generic.list_detail import object_list
from django.conf import settings
from tagging.views import tagged_object_list

IMAGESTORE_ON_PAGE = getattr(settings, 'IMAGESTORE_ON_PAGE', 12)
IMAGESTORE_STORAGE_PREVIEW = getattr(settings, 'IMAGESTORE_STORAGE_PREVIEW', 5)

def filter_access(request):
    '''
    Filter images/categories that current user can access
    '''
    filter = {}
    if not request.user.is_staff:
        filter['is_public'] = True
    return filter

def set_storage_preview(storage, images=None):
    '''
    Add .preview attribute list to storage object
    containing X last images from images queryset or from storage.images queryset
    filter only public images
    '''
    if images is None:
        images = storage.images
    storage.preview = images.filter(is_public=True).all()[:IMAGESTORE_STORAGE_PREVIEW]

def category(request, slug=None):
    '''
    Category view
    Filter images for current user access from current category
    List descendants categories of category or all root categories if no slug defined
    '''
    filter = filter_access(request)
    if slug:
        category = get_object_or_404(Category, slug=slug)
        if not (request.user.is_staff or category.is_public):
            return HttpResponseForbidden()
        category_list = category.get_descendants().filter(**filter)
        images = category.images.filter(**filter)
    else:
        category = None
        category_list = Category.tree.root_nodes().filter(**filter)
        images = Image.objects.filter(**filter).all()
    category_list = list(category_list)
    map(set_storage_preview, category_list)
    kwargs = {'queryset': images,
              'template_object_name': 'image',
              'template_name': 'imagestore/category.html',
              'paginate_by': IMAGESTORE_ON_PAGE,
              'extra_context': {'category': category, 'category_list': category_list}}
    return object_list(request, **kwargs)

def tag(request, tag):
    '''
    List tagged images
    '''
    filter = filter_access(request)
    kwargs = {
        'queryset_or_model': Image.objects.filter(**filter),
        'template_object_name': 'image',
        'template_name': 'imagestore/tag.html',
        'paginate_by': IMAGESTORE_ON_PAGE,
        'tag': tag,
    }
    return tagged_object_list(request, **kwargs)

    