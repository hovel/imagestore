Installation
============

* Install with pip or easy install (All dependencies will be installed automatically)::

    pip install imagestore
    
* Symlink or copy `imagestore/static/imagestore.css` to your `MEDIA_ROOT`, or write youre own style (staticfiles supported as well).
* Add `imagestore`, `django-tagging` and `sorl.thumbnail` to your `INSTALLED_APPS`.
  your `INSTALLED_APPS` should look like::

    INSTALLED_APPS = (
        ....
        'imagestore',
        'sorl.thumbnail',
        'tagging',
        'south' # Optionally but recommended
    )

* Add `imagestore.urls` to your urls with `namespace='imagestore'`::

    urlpatterns = patterns('',
        ......
        (r'^gallery/', include('imagestore.urls', namespace='imagestore')),
        ......
    )

* Set `IMAGESTORE_SHOW_USER` to False, if you don't want to show information from user profile or have no user profile.

* Run::

        ./manage.py syncdb

  or::

        ./manage.py migrate

* Add jquery and jqueryui load to your template to use tagging autocomplete and/or prettyphoto
* If you want to use prettyPhoto put `prettyPhoto <http://www.no-margin-for-errors.com/projects/prettyphoto-jquery-lightbox-clone/>`_ to your media directory and include imagesotore/prettyphoto.html to your template