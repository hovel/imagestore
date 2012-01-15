from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.utils.decorators import method_decorator
from imagestore.models import Album, Image
from imagestore.models import image_applabel, image_classname
from imagestore.models import album_applabel, album_classname
from django.shortcuts import get_object_or_404
from django.http import  Http404, HttpResponseRedirect
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from tagging.models import TaggedItem
from tagging.utils import get_tag
from django.contrib.contenttypes.models import ContentType
from utils import load_class
from django.db.models import Q

IMAGESTORE_IMAGES_ON_PAGE = getattr(settings, 'IMAGESTORE_IMAGES_ON_PAGE', 20)

IMAGESTORE_ON_PAGE = getattr(settings, 'IMAGESTORE_ON_PAGE', 20)

ImageForm = load_class(getattr(settings, 'IMAGESTORE_IMAGE_FORM', 'imagestore.forms.ImageForm'))
AlbumForm = load_class(getattr(settings, 'IMAGESTORE_ALBUM_FORM', 'imagestore.forms.AlbumForm'))

class AlbumListView(ListView):
    context_object_name = 'album_list'
    template_name = 'imagestore/album_list.html'
    paginate_by = getattr(settings, 'IMAGESTORE_ALBUMS_ON_PAGE', 20)
    allow_empty = True

    def get_queryset(self):
        albums = Album.objects.filter(is_public=True).select_related('head')
        self.e_context = dict()
        if 'username' in self.kwargs:
            user = get_object_or_404(User, username=self.kwargs['username'])
            albums = albums.filter(user=user)
            self.e_context['view_user'] = user
        return albums

    def get_context_data(self, **kwargs):
        context = super(AlbumListView, self).get_context_data(**kwargs)
        context.update(self.e_context)
        return context


def get_images_queryset(self):
    images = Image.objects.all()
    self.e_context = dict()
    if 'tag' in self.kwargs:
        tag_instance = get_tag(self.kwargs['tag'])
        if tag_instance is None:
            raise Http404(_('No Tag found matching "%s".') % self.kwargs['tag'])
        self.e_context['tag'] = tag_instance
        images = TaggedItem.objects.get_by_model(images, tag_instance)
    if 'username' in self.kwargs:
        user = get_object_or_404(User, username=self.kwargs['username'])
        self.e_context['view_user'] = user
        images = images.filter(user=user)
    if 'album_id' in self.kwargs:
        album = get_object_or_404(Album, id=self.kwargs['album_id'])
        self.e_context['album'] = album
        images = images.filter(album=album)
        if (not album.is_public) and\
           (self.request.user != album.user) and\
           (not self.request.user.has_perm('imagestore.moderate_albums')):
            raise PermissionDenied
    return images


class ImageListView(ListView):
    context_object_name = 'image_list'
    template_name = 'imagestore/image_list.html'
    paginate_by = getattr(settings, 'IMAGESTORE_IMAGES_ON_PAGE', 20)
    allow_empty = True

    get_queryset = get_images_queryset

    def get_context_data(self, **kwargs):
        context = super(ImageListView, self).get_context_data(**kwargs)
        context.update(self.e_context)
        return context


class ImageView(DetailView):
    context_object_name = 'image'
    template_name = 'imagestore/image.html'

    get_queryset = get_images_queryset

    def get_context_data(self, **kwargs):
        context = super(ImageView, self).get_context_data(**kwargs)
        image = context['image']
        # Check thant album is public or user have rights to see it
        if image.album:
            if (not image.album.is_public) and\
               (self.request.user != image.album.user) and\
               (not self.request.user.has_perm('imagestore.moderate_albums')):
                raise PermissionDenied
        base_qs = self.get_queryset()
        count = base_qs.count()
        img_pos = base_qs.filter(
            Q(order__lt=image.order)|
            Q(id__lt=image.id, order=image.order)
        ).count()
        next = None
        previous = None
        if count - 1 > img_pos:
            try:
                next = base_qs.filter(
                    Q(order__gt=image.order)|
                    Q(id__gt=image.id, order=image.order)
                )[0]
            except IndexError:
                pass
        if img_pos > 0:
            try:
                previous = base_qs.filter(
                    Q(order__lt=image.order)|
                    Q(id__lt=image.id, order=image.order)
                ).order_by('-order', '-id')[0]
            except IndexError:
                pass
        context['next'] = next
        context['previous'] = previous
        context.update(self.e_context)
        return context


class CreateAlbum(CreateView):
    template_name = 'imagestore/forms/album_form.html'
    model = Album
    form_class = AlbumForm

    @method_decorator(login_required)
    @method_decorator(permission_required('%s.add_%s' % (album_applabel, album_classname)))
    def dispatch(self, *args, **kwargs):
        return super(CreateAlbum, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


def filter_album_queryset(self):
    if self.request.user.has_perm('imagestore.moderate_albums'):
        return Album.objects.all()
    else:
        return Album.objects.filter(user=self.request.user)


class UpdateAlbum(UpdateView):
    template_name = 'imagestore/forms/album_form.html'
    model = Album
    form_class = AlbumForm

    get_queryset = filter_album_queryset

    @method_decorator(login_required)
    @method_decorator(permission_required('%s.add_%s' % (album_applabel, album_classname)))
    def dispatch(self, *args, **kwargs):
        return super(UpdateAlbum, self).dispatch(*args, **kwargs)


class DeleteAlbum(DeleteView):
    template_name = 'imagestore/album_delete.html'
    model = Album

    def get_success_url(self):
        return reverse('imagestore:index')

    get_queryset = filter_album_queryset

    @method_decorator(login_required)
    @method_decorator(permission_required('%s.change_%s' % (album_applabel, album_classname)))
    def dispatch(self, *args, **kwargs):
        return super(DeleteAlbum, self).dispatch(*args, **kwargs)


class CreateImage(CreateView):
    template_name = 'imagestore/forms/image_form.html'
    model = Image
    form_class = ImageForm

    @method_decorator(login_required)
    @method_decorator(permission_required('%s.add_%s' % (image_applabel, image_classname)))
    def dispatch(self, *args, **kwargs):
        return super(CreateImage, self).dispatch(*args, **kwargs)

    def get_form(self, form_class):
        return form_class(user=self.request.user, **self.get_form_kwargs())

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        if self.object.album:
            self.object.album.save()
        return HttpResponseRedirect(self.get_success_url())


def get_edit_image_queryset(self):
    if self.request.user.has_perm('%s.moderate_%s' % (image_applabel, image_classname)):
        return Image.objects.all()
    else:
        return Image.objects.filter(user=self.request.user)


class UpdateImage(UpdateView):
    template_name = 'imagestore/forms/image_form.html'
    model = Image
    form_class = ImageForm

    get_queryset = get_edit_image_queryset

    def get_form(self, form_class):
        return form_class(user=self.object.user, **self.get_form_kwargs())

    @method_decorator(login_required)
    @method_decorator(permission_required('%s.change_%s' % (image_applabel, image_classname)))
    def dispatch(self, *args, **kwargs):
        return super(UpdateImage, self).dispatch(*args, **kwargs)


class DeleteImage(DeleteView):
    template_name = 'imagestore/image_delete.html'
    model = Image

    def get_success_url(self):
        return reverse('imagestore:index')

    get_queryset = get_edit_image_queryset

    @method_decorator(login_required)
    @method_decorator(permission_required('%s.delete_%s' % (image_applabel, image_classname)))
    def dispatch(self, *args, **kwargs):
        return super(DeleteImage, self).dispatch(*args, **kwargs)