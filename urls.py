from django.conf.urls.defaults import *
from imagestore.views import image


images = url(
    regex = '^image/(?P<slug_or_id>[^/]+)/$',
    view = 'imagestore.views.image',
    name = 'imagestore-image'
)

category = url(
    regex = '^(?P<slug>[^/]+)/$',
    view = 'imagestore.views.category',
    name = 'imagestore-category'
)

category_list = url(
    regex = '^$',
    view = 'imagestore.views.category_list',
    name = 'imagestore-category-list'
)
urlpatterns = patterns('', images, category, category_list)



