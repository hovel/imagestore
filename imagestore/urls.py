from django.conf.urls.defaults import *
from models import Image
from tagging.models import Tag

from fancy_autocomplete.views import AutocompleteSite
autocomletes = AutocompleteSite()

autocomletes.register(
    'tag',
    queryset=Tag.objects.all(),
    search_fields=('name',),
    limit=10
)

urlpatterns = patterns('imagestore.views',
                       url(r'^$', 'category', name='imagestore-category-list'),
                       url(r'^category/(?P<slug>[-\w]+)/$','category', name='imagestore-category'),
                       url(r'^tag/(?P<tag>[^/]+)/$', 'tag', name='imagestore-tag'),
                       url(r'^user/(?P<username>\w+)/$', 'user_gallery', name='imagestore-user'),
                       url(r'^upload/$', 'image_add', name='imagestore-upload'),
                       url(r'^image/(?P<id>\d+)/$', 'image', name='imagestore-image'),
                       url(r'^image/(?P<id>\d+)/delete/$', 'delete_image', name='imagestore-delete'),
                       url(r'^image/(?P<id>\d+)/update/$', 'update_image', name='imagestore-update'),
                       url(r'^autocomplete/(.*)/$', autocomletes, name='imagestore-autocomplete-tag')
                       )



