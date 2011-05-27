ImageStore
==========

An image gallery, created for easy integration for an exiting django project.
Very ligth, builded around django generic views

Features:
=========
* Optional PrettyPhoto for image/album show
* Albums
* Tagging support
* South support for upgrades


Installation:
=============

* Install with pip or easy install (All dependencies will be installed automatically)
* Symlink or copy imagestore/static/imagestore.css to your MEDIA_ROOT, or write youre own style (staticfiles supported as well).
* Add imagestore to your INSTALLED_APPS
* Add imagestore.urls to your urls with `namespace='imagestore'`
* Set `IMAGESTORE_SHOW_USER` to False, if you don't want to show information from user profile or have no user profile.
* Run ./manage.py syncdb or ./manage.py migrate
* Add jquery and jqueryui load to your template to use tagging autocomplete and/or prettyphoto
* If you want to use prettyPhoto put `prettyPhoto <http://www.no-margin-for-errors.com/projects/prettyphoto-jquery-lightbox-clone/>`__ to your media directory and include imagesotore/prettyphoto.html to your template

Configuration:
==============
If IMAGESTORE_SELF_MANAGE is True (default), all created users will get add/delete/change permissions for Images and Albums. If you don't wish users to create albums or upload images set this property to false.


Django CMS Integration:
=======================

Imagestore can show an album as a plugin in django-cms, and can be used as djang-cms app.

To use plugin, just add `imagestore.cms` to your INSTALLED_APPS

If you want to use imagesotore a djang-cms application, you need to tell django where to search imagestore namespace,
you can do it by adding django-cms urls with 'imagestore' namespace::

    url(r'^', include('cms.urls')),
    url(r'^', include('cms.urls', namespace='imagestore'))


Translation:
============

* Russian
* English

Watermarking:
=============

Use `watermarker <http://pypi.python.org/pypi/watermarker/>`__ sorl integration to add watermark to your images

