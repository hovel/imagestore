from django.conf.urls.defaults import *

urlpatterns = patterns('imagestore.views',
                       url(r'^$', 'category', name='imagestore-category-list'),
                       url(r'^category/(?P<slug>[-\w]+)/$','category', name='imagestore-category'),
                       url(r'^tag/(?P<tag>[^/]+)/$', 'tag', name='imagestore-tag'),
                       url(r'^user/(?P<username>\w+)/$', 'user_gallery', name='imagestore-user')
                       )



