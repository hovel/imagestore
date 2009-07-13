from django.http import HttpResponse
from imagestore.models import Image, Category
from django.http import Http404
from django.shortcuts import render_to_response
from django.views.generic.list_detail import object_list
from django.template import RequestContext

#import logging

PREVIEW_LIST = 2

def category(request, slug, *args, **kwargs):
    try:
        category = Category.objects.get(slug=slug)
    except:
        raise Http404

    kwargs['queryset'] = Image.objects.filter(category=category).all()
    #logging.debug(kwargs['queryset'].count())
    kwargs['template_object_name'] = 'images'
    kwargs['paginate_by'] = 9
    kwargs['template_name'] = 'imagestore/category.html'
    kwargs['extra_context'] = {'category': category}
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

    images_after = list(Image.objects.filter(category=image.category, id__gt=image.id).order_by('id'))
    images_before = list(Image.objects.filter(category=image.category, id__lt=image.id).order_by('id'))
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
    categories = Category.objects.all()
    return render_to_response('imagestore/gallery.html', {'categories_list': categories}, context_instance=RequestContext(request))
