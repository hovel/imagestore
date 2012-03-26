Django CMS Integration
======================

Imagestore supports integration with `django-cms
<https://www.django-cms.org/>`_ both as a plugin and as an application.

As a plugin
-----------------------------
To use plugins, just add ``imagestore.imagestore_cms`` to your
``INSTALLED_APPS``.
The default templates used by the plugins make use of
`sekizai tags <https://github.com/ojii/django-sekizai>`_ to add the
required javascript to the rendered page.
If you are using django-cms 2.2 and later, this is the suggested
way to add any required javascript. For older versions of django-cms,
you should instead use the included ``*_pre2.2.html`` versions of
the templates.

As an application
-----------------------------
If you want to use imagesotore as django-cms application:

* Set `IMAGESTORE_SHOW_USER` to `False`
* Beacause django-cms build connect apps without namespace settings
  you need to tell django where to search imagestore namespace,
  you can do it by adding django-cms urls with 'imagestore' namespace::

    url(r'^', include('cms.urls')),
    url(r'^', include('cms.urls', namespace='imagestore'))
