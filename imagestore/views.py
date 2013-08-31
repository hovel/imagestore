import os
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.utils.decorators import method_decorator
from imagestore.models import Album, Image
from imagestore.models import image_applabel, image_classname
from imagestore.models import album_applabel, album_classname
from django.shortcuts import get_object_or_404
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _
from django.utils import simplejson
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from tagging.models import TaggedItem
from tagging.utils import get_tag
from utils import load_class
from django.db.models import Q
from actstream import action
from mezzanine.blog.models import BlogPost
from sorl.thumbnail import delete
from actstream.models import Action
from django.contrib.contenttypes.models import ContentType

try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
    username_field = User.USERNAME_FIELD
except ImportError:
    from django.contrib.auth.models import User
    username_field = 'username'

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
            user = get_object_or_404(**{'klass': User, username_field: self.kwargs['username']})
            albums = albums.filter(user=user)
            self.e_context['view_user'] = user
            self.e_context['max_images'] = getattr(settings, 'MAX_IMAGES_PER_VENDOR', 50)
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
        user = get_object_or_404(**{'klass': User, username_field: self.kwargs['username']})
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

class ImageListTemplateView(ListView):
    context_object_name = 'image_list'
    template_name = 'imagestore/render_image_list.html'
    paginate_by = getattr(settings, 'IMAGESTORE_IMAGES_ON_PAGE', 20)
    allow_empty = True

    get_queryset = get_images_queryset

    def get_context_data(self, **kwargs):
        context = super(ImageListTemplateView, self).get_context_data(**kwargs)
        context.update(self.e_context)
        return context

class ImageListMinView(ListView):
    context_object_name = 'image_list'
    template_name = 'imagestore/render_image_min_list.html'
    #paginate_by = getattr(settings, 'IMAGESTORE_IMAGES_ON_PAGE', 20)
    allow_empty = True

    #get_queryset = get_images_queryset
    def get_queryset(self):
        images = Image.objects.all().order_by('-created')
        self.e_context = dict()
        if 'tag' in self.kwargs:
            tag_instance = get_tag(self.kwargs['tag'])
            if tag_instance is None:
                raise Http404(_('No Tag found matching "%s".') % self.kwargs['tag'])
            self.e_context['tag'] = tag_instance
            images = TaggedItem.objects.get_by_model(images, tag_instance)
        if 'username' in self.kwargs:
            user = get_object_or_404(**{'klass': User, username_field: self.kwargs['username']})
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

    def get_context_data(self, **kwargs):
        context = super(ImageListMinView, self).get_context_data(**kwargs)
        offset= self.kwargs.get('offset', -1)
        context.update(self.e_context)
        context["offset"] = int(offset)
        return context

class ImageListExView(ListView):
    context_object_name = 'image_list'
    template_name = 'imagestore/render_image_ex_list.html'
    #paginate_by = getattr(settings, 'IMAGESTORE_IMAGES_ON_PAGE', 20)
    allow_empty = True

    get_queryset = get_images_queryset
                
    def get_context_data(self, **kwargs):
        context = super(ImageListExView, self).get_context_data(**kwargs)
        exclude_id= self.kwargs.get('exclude', -1)
        context.update(self.e_context)
        context["exclude_id"] = int(exclude_id)
        return context

class ImageView(DetailView):
    context_object_name = 'image'
    template_name = 'imagestore/image.html'

    get_queryset = get_images_queryset

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.album:
            if (not self.object.album.is_public) and\
               (self.request.user != self.object.album.user) and\
               (not self.request.user.has_perm('imagestore.moderate_albums')):
                raise PermissionDenied

        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(ImageView, self).get_context_data(**kwargs)
        image = context['image']

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

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        user = request.user
        blog_posts = BlogPost.objects.published(for_user=user).select_related().filter(user=user)

        if blog_posts and blog_posts[0]:
            blog_post = blog_posts[0]
            blog_post.num_images = blog_post.num_images - self.object.images.all().count()
            blog_post.save()

        for image in self.object.images.all():
            delete(image.image)
            image.delete()

        media_root = getattr(settings, 'MEDIA_ROOT', '/')
        album_dir = self.object.get_album_path()
        album_abs_dir = os.path.join(media_root, album_dir)
        os.rmdir(album_abs_dir)
        
        self.object.delete()
        return HttpResponseRedirect(self.get_success_url())

def json_error_response(error_message):
    return HttpResponse(simplejson.dumps(dict(success=False,
                                              error_message=error_message)))

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

		user = self.request.user
		blog_posts = BlogPost.objects.published(for_user=user).select_related().filter(user=user)
		if blog_posts and blog_posts[0]:
			blog_post = blog_posts[0]
			if blog_post.num_images < getattr(settings, 'MAX_IMAGES_PER_VENDOR', 10):
				blog_post.num_images += 1
				blog_post.save()
				self.object = form.save(commit=False)
				self.object.user = self.request.user
				self.object.save()
				if self.object.album:
					self.object.album.save()
					if self.object.album.images.all().count() == 1:
						action.send(blog_post, verb=settings.ALBUM_ADD_VERB, target=self.object.album)
					else:
						ctype = ContentType.objects.get_for_model(blog_post)
						target_content_type = ContentType.objects.get_for_model(self.object.album)
						Action.objects.all().filter(actor_content_type=ctype, actor_object_id=blog_post.id, verb=settings.ALBUM_ADD_IMAGE_VERB, target_content_type=target_content_type, target_object_id=self.object.album.id ).delete()
						action.send(blog_post, verb=settings.ALBUM_ADD_IMAGE_VERB, target=self.object.album)
				return HttpResponseRedirect(self.get_success_url())
			else:    
				return json_error_response("'%s' has crossed maximum limit of images" % user)

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

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.image:
            delete(self.object.image)
        self.object.delete()
        user = request.user
        blog_posts = BlogPost.objects.published(for_user=user).select_related().filter(user=user)
        if blog_posts and blog_posts[0]:
            blog_post = blog_posts[0]
            blog_post.num_images = blog_post.num_images - 1
            blog_post.save() 
        return HttpResponseRedirect(self.get_success_url())

        