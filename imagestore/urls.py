from django.conf.urls.defaults import *


#images = url(
#    regex = '^image/(?P<slug_or_id>[^/]+)/$',
#    view = 'imagestore.views.image',
#    name = 'imagestore-image'
#)

category = url(
    regex = '^(?P<slug>[^/]+)/$',
    view = 'imagestore.views.category',
    name = 'imagestore-category'
)

#author = url(
#    regex = '^author/(?P<slug>[^/]+)/$',
#    view = 'imagestore.views.author',
#    name = 'imagestore-author'
#)

category_list = url(
    regex = '^$',
    view = 'imagestore.views.category_list',
    name = 'imagestore-category-list'
)
urlpatterns = patterns('', category, category_list)



