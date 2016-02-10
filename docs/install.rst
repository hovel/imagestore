Installation for Python 2 and Django 1.7
========================================

* Install with pip or easy install (All dependencies will be installed automatically, however if you use Python 3 you may need to install specific versions of ``sorl-thunbmail`` and ``django-autocomplete-light``)::

    pip install imagestore

* If you use django before version 1.7 we recomment to install south for smooth migrations::

    pip install south

* Symlink or copy `imagestore/static/imagestore.css` to your `MEDIA_ROOT`, or write youre own style (staticfiles supported as well).
* Add `imagestore`, `django-tagging` and `sorl.thumbnail` to your `INSTALLED_APPS`.
  your `INSTALLED_APPS` should look like::

    INSTALLED_APPS = (
        ....
        'imagestore',
        'sorl.thumbnail',
        'tagging',
    )

* Add `imagestore.urls` to your urls with `namespace='imagestore'`::

    urlpatterns = patterns('',
        ......
        (r'^gallery/', include('imagestore.urls', namespace='imagestore')),
        ......
    )

* Set `IMAGESTORE_SHOW_USER` to False, if you don't want to show information from user profile or have no user profile.

* Run::

        ./manage.py migrate

* Add jquery and jqueryui load to your template to use tagging autocomplete and/or prettyphoto
* If you want to use prettyPhoto put `prettyPhoto <http://www.no-margin-for-errors.com/projects/prettyphoto-jquery-lightbox-clone/>`_ to your media directory and include imagesotore/prettyphoto.html to your template

Installation for Python 3 and Django 1.9
========================================

* Install sorl-thumbnail. As the version in pip misses migration, one of the
  solution is to install v12.4a1 from GitHub::

    pip install git+git://github.com/mariocesar/sorl-thumbnail@v12.4a1

   More can be found concerning this subject on the following
   StackOverflow question:
   http://stackoverflow.com/questions/35136411/table-thumbnail-kvstore-doesnt-exist

* Install Pillow (a fork of PIL for Python 3)::

    pip install pillow

* Install chardet::
  
    pip install chardet

* Install imagestore. Since the current version in pip is not compatible with Django
  1.9 use the one on GitHub::

    pip install git+git://github.com/hovel/imagestore

* Symlink or copy `imagestore/static/imagestore.css` to your `MEDIA_ROOT`, or write youre own style (staticfiles supported as well).

* Add `imagestore`, `django-tagging` and `sorl.thumbnail` to your `INSTALLED_APPS`.
  your `INSTALLED_APPS` should look like::

    INSTALLED_APPS = (
        ....
        'imagestore',
        'sorl.thumbnail',
        'tagging',
    )

* Add `imagestore.urls` to your urls with `namespace='imagestore'`::

    urlpatterns = patterns('',
        ......
        (r'^gallery/', include('imagestore.urls', namespace='imagestore')),
        ......
    )
    
* Set `IMAGESTORE_SHOW_USER` to False, if you don't want to show information from user profile or have no user profile.

* Set the media URL (it does not necesseraly need to be media)::

    MEDIA_URL = "/media/"
    
* Set the media root. The directory must already exist. We assume here that the BASE_DIR variable has been setup. You could also hard code the absolute path but it would be much less flexible...::

    MEDIA_ROOT = os.path.join(BASE_DIR, "media/")

* Specify a template directory (which must already exist). We named it "templates" in this example::

    TEMPLATES = [
        {
            ...
            'DIRS': [os.path.join(BASE_DIR, "templates/")],
            ...
        },
    ]

* Create a template named base.html in your templates directory (the one you have defined just above). The important aspect is that it must have a `{% block content %}`. You will find below a very basic example::

    {% load staticfiles %}
    <html>
        <head>
            <title>
                {% block title %}Kitchensink{% endblock title %}
            </title>
            {% block stylesheets %}
            <link rel="stylesheet" type="text/css" href="{% static "css/project.css" %}">
            {% endblock stylesheets %}
         </head>
        <body>
            <div class="content">
                {% block content %}
                <h1>Example project</h1>
                {% endblock content %}
            </div>
        </body>
    </html>

* Run::

        ./manage.py migrate

* Add jquery and jqueryui load to your template to use tagging autocomplete and/or prettyphoto
* If you want to use prettyPhoto put `prettyPhoto <http://www.no-margin-for-errors.com/projects/prettyphoto-jquery-lightbox-clone/>`_ to your media directory and include imagesotore/prettyphoto.html to your template
