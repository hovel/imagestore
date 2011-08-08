from django.conf.urls.defaults import *
from tagging.models import Tag
from views import AlbumListView, ImageListView, UpdateImage, UpdateAlbum, CreateImage, CreateAlbum, DeleteImage, DeleteAlbum, ImageView

from fancy_autocomplete.views import AutocompleteSite
autocomletes = AutocompleteSite()

autocomletes.register(
    'tag',
    queryset=Tag.objects.all(),
    search_fields=('name',),
    limit=10,
    lookup='istartswith',
)


urlpatterns = patterns('imagestore.views',
                       url(r'^$', AlbumListView.as_view(), name='index'),


                       url(r'^album/add/$', CreateAlbum.as_view(), name='create-album'),
                       url(r'^album/(?P<album_id>\d+)/$', ImageListView.as_view(), name='album'),
                       url(r'^album/(?P<pk>\d+)/edit/$', UpdateAlbum.as_view(), name='update-album'),
                       url(r'^album/(?P<pk>\d+)/delete/$', DeleteAlbum.as_view(), name='delete-album'),

                       url(r'^tag/(?P<tag>[^/]+)/$', ImageListView.as_view(), name='tag'),

                       url(r'^user/(?P<username>\w+)/albums', AlbumListView.as_view(), name='user'),
                       url(r'^user/(?P<username>\w+)/$', ImageListView.as_view(), name='user-images'),

                       url(r'^upload/$', CreateImage.as_view(), name='upload'),

                       url(r'^image/(?P<pk>\d+)/$', ImageView.as_view(), name='image'),
                       url(r'^album/(?P<album_id>\d+)/image/(?P<pk>\d+)/$', ImageView.as_view(), name='image-album'),
                       url(r'^tag/(?P<tag>[^/]+)/image/(?P<pk>\d+)/$', ImageView.as_view(), name='image-tag'),
                       url(r'^image/(?P<pk>\d+)/delete/$', DeleteImage.as_view(), name='delete-image'),
                       url(r'^image/(?P<pk>\d+)/update/$', UpdateImage.as_view(), name='update-image'),

                       url(r'^autocomplete/(.*)/$', autocomletes, name='autocomplete')
                       )



