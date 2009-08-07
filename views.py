from django.http import HttpResponse, HttpResponseForbidden
from imagestore.models import Image, Category
from persons.models import Person
from django.http import Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.views.generic.list_detail import object_list
from django.template import RequestContext
from django.conf import settings
from django.core.cache import cache
from django.db.models.signals import post_save, pre_delete


IMAGESTORE_ON_PAGE = getattr(settings, 'IMAGESTORE_ON_PAGE', 12)

def filter_image_access(request, category=None, author=None):
    '''
    Filter images that current user can access
    '''
    filter = {}
    if not request.user.is_staff:
        filter['is_public'] = True
        filter['author__is_public'] = True

    return filter
   
def category(request, slug, *args, **kwargs):
    category = get_object_or_404(Category, slug=slug)
    if not (request.user.is_staff or category.is_public):
        return HttpResponseForbidden()
    authors = Person.objects.filter(is_public=True).order_by('order')
    filter = filter_image_access(request)
    kwargs['queryset'] = Image.objects.filter(**filter).filter(category=category).order_by('order', 'author__order', 'id')
    kwargs['template_object_name'] = 'images'
    kwargs['paginate_by'] = IMAGESTORE_ON_PAGE
    kwargs['template_name'] = 'imagestore/category.html'
    kwargs['extra_context'] = {'category': category, 'author_list': authors}
    return object_list(request, *args, **kwargs)

def author(request, slug, *args, **kwargs):
    author = get_object_or_404(Person, slug=slug)
    if not (request.user.is_staff or author.is_public):
        return HttpResponseForbidden()
    authors = Person.objects.all().order_by('order')
    filter = filter_image_access(request)
    filter['author'] = author
    kwargs['queryset'] = Image.objects.filter(**filter).order_by('order', 'id')
    kwargs['template_object_name'] = 'images'
    kwargs['paginate_by'] = IMAGESTORE_ON_PAGE
    kwargs['template_name'] = 'imagestore/author.html'
    kwargs['extra_context'] = {'author': author, 'author_list': authors}
    return object_list(request, *args, **kwargs)



def image(request, slug_or_id):
    try:
        image = Image.objects.get(id=slug_or_id)
    except:
        try:
            image = Image.objects.get(slug=slug_or_id)
        except:
            raise Http404
    if not (request.user.is_staff or image.is_public):
        return HttpResponseForbidden()
    filter = filter_image_access(request)
    response = {}
    response['image'] = image
    images = list(Image.objects.filter(category=image.category).filter(**filter).order_by('order', 'author__order', 'id'))
    response['images'] = images
    response['previous'] = None
    response['next'] = None
    last = len(images)-1
    for i, img in enumerate(images):
        if img.id == image.id:
            img.current = True
            if i > 0:
                response['previous'] = images[i-1]
            if i < last:
                response['next'] = images[i+1]
            break
    response['category'] = image.category
    return render_to_response('imagestore/image.html', response, context_instance=RequestContext(request))

def category_list(request):
    categories = Category.objects.order_by('order')
    return render_to_response('imagestore/gallery.html', {'categories_list': categories}, context_instance=RequestContext(request))
