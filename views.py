from django.http import HttpResponse
from imagestore.models import Image, Category
from persons.models import Person
from django.http import Http404
from django.shortcuts import render_to_response get_object_or_404
from django.views.generic.list_detail import object_list
from django.template import RequestContext
from django.conf import settings


IMAGESTORE_ON_PAGE = settings.getattr(IMAGESTORE_ON_PAGE, 12)

def category(request, slug, *args, **kwargs):
    category = get_object_or_404(Category, slug=slug)
    authors = Person.objects.all().order_by('order')
    kwargs['queryset'] = Image.objects.filter(category=category).order_by('order', 'author__order', 'id')
    kwargs['template_object_name'] = 'images'
    kwargs['paginate_by'] = IMAGESTORE_ON_PAGE
    kwargs['template_name'] = 'imagestore/category.html'
    kwargs['extra_context'] = {'category': category, 'authors': author_list}
    return object_list(request, *args, **kwargs)

def author(request, slug, *args, **kwargs):
    author = get_object_or_404(Persons, slug=slug)
    kwargs['queryset'] = Image.objects.filter(author=author).order_by('order', 'id')
    kwargs['template_object_name'] = 'images'
    kwargs['paginate_by'] = IMAGESTORE_ON_PAGE
    kwargs['template_name'] = 'imagestore/author.html'
    kwargs['extra_context'] = {'author': author}
    return object_list(request, *args, **kwargs)



def image(request, slug_or_id):
    try:
        image = Image.objects.get(slug=slug_or_id)
    except:
        try:
            image = Image.objects.get(id=slug_or_id)
        except:
            raise Http404
    result = {}
    images_after = list(Image.objects.filter(category=image.category, id__gt=image.id).order_by('order', 'id'))
    images_before = list(Image.objects.filter(category=image.category, id__lt=image.id).order_by('order', 'id'))
    images = [image]
    image.current = True
    previous = None
    next = None
    if len(images_before) > 0:
        previous = images_before[-1]
        images = images_before + images
    if len(images_after) > 0:
        next = images_after[0]
        images += list(images_after)
    return render_to_response('imagestore/image.html', {'image': image, 'images': images, 'previous': previous, 'next': next, 'category': image.category}, context_instance=RequestContext(request))

def category_list(request):
    categories = Category.objects.order_by('order')
    return render_to_response('imagestore/gallery.html', {'categories_list': categories}, context_instance=RequestContext(request))
