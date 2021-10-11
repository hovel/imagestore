# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.urls import re_path
from .views import AlbumListView, ImageListView, UpdateImage, UpdateAlbum, \
    CreateImage, CreateAlbum, DeleteImage, DeleteAlbum, ImageView, \
    ImageTagAutocompleteView

app_name = 'imagestore'

urlpatterns = [
    re_path(r'^$', AlbumListView.as_view(), name='index'),

    re_path(r'^album/add/$', CreateAlbum.as_view(), name='create-album'),
    re_path(r'^album/(?P<album_id>\d+)/$', ImageListView.as_view(), name='album'),
    re_path(r'^album/(?P<pk>\d+)/edit/$', UpdateAlbum.as_view(), name='update-album'),
    re_path(r'^album/(?P<pk>\d+)/delete/$', DeleteAlbum.as_view(), name='delete-album'),

    re_path(r'^tag/(?P<tag>[^/]+)/$', ImageListView.as_view(), name='tag'),

    re_path(r'^user/(?P<username>\w+)/albums/', AlbumListView.as_view(), name='user'),
    re_path(r'^user/(?P<username>\w+)/$', ImageListView.as_view(), name='user-images'),

    re_path(r'^upload/$', CreateImage.as_view(), name='upload'),

    re_path(r'^image/(?P<pk>\d+)/$', ImageView.as_view(), name='image'),
    re_path(r'^album/(?P<album_id>\d+)/image/(?P<pk>\d+)/$', ImageView.as_view(), name='image-album'),
    re_path(r'^tag/(?P<tag>[^/]+)/image/(?P<pk>\d+)/$', ImageView.as_view(), name='image-tag'),
    re_path(r'^image/(?P<pk>\d+)/delete/$', DeleteImage.as_view(), name='delete-image'),
    re_path(r'^image/(?P<pk>\d+)/update/$', UpdateImage.as_view(), name='update-image'),

    re_path(r'^tag-autocomplete/$', ImageTagAutocompleteView.as_view(), name='tag-autocomplete'),
]
