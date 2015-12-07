Installation
============

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
