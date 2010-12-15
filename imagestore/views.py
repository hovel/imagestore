from imagestore.models import Category, Image
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseForbidden
from django.views.generic.list_detail import object_list
from django.conf import settings
from django.contrib.auth.models import User
from tagging.views import tagged_object_list
from django.contrib.auth.decorators import login_required
from forms import ImageForm
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from django.views.generic.simple import direct_to_template
from django.views.generic.create_update import delete_object, update_object

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

def user_gallery(request, username):
    '''
    List images uploaded by target user
    '''
    filter = filter_access(request)
    user = get_object_or_404(User, username=username)
    filter['user'] = user
    kwargs = {
        'queryset': Image.objects.filter(**filter),
        'template_object_name': 'image',
        'template_name': 'imagestore/user.html',
        'paginate_by': IMAGESTORE_ON_PAGE,
        'extra_context': {'gallery_owner': user}
    }
    return object_list(request, **kwargs)

@login_required
def image_add(request):
    '''
    Show form for image uploading
    '''
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.user = request.user
            image.save()
            msg = _("Image was created successfully.")
            messages.success(request, msg, fail_silently=True)
            return redirect(image.get_absolute_url())
    else:
        form = ImageForm()
    return direct_to_template(request, template='imagestore/image-form.html', extra_context={'form': form})

@login_required
def delete_image(request, id):
    image = get_object_or_404(Image, id=id)
    if not (request.user.is_superuser or request.user == image.user):
        return HttpResponseForbidden
    return delete_object(request, Image, object_id=id, post_delete_redirect=image.category.get_absolute_url())

@login_required
def update_image(request, id):
    image = get_object_or_404(Image, id=id)
    if not (request.user.is_superuser or request.user == image.user):
        return HttpResponseForbidden
    return update_object(request, Image, object_id=id,
                         post_save_redirect=image.get_absolute_url(),
                         form_class=ImageForm,
                         template_name='imagestore/image-form.html')

def image(request, id):
    '''
    Check premissions and ouput an image
    '''
    image = get_object_or_404(Image, id=id)
    if (not image.is_public) and (not request.user.is_superuser) and (not image.user == request.user):
        return HttpResponseForbidden()
        #TODO Show gallery/user
    return direct_to_template(request, template='imagestore/image.html', extra_context={'image': image})
    