Extending Imagestore
====================

You can extend imagestore by customizing Image and Album classes
as well as forms for their creation. Basic abstract classes that
require to extend exists in ``models.bases.image`` and ``models.bases.album``.

After you create your classes, tell imagestore to use them by setting next settings:

* IMAGESTORE_IMAGE_MODEL
* IMAGESTORE_ALBUM_MODEL
* IMAGESTORE_IMAGE_FORM
* IMAGESTORE_ALBUM_FORM

You should set model-related settings to ``app_label.model_name`` string. For example::

    IMAGESTORE_IMAGE_MODEL = 'mystoreapp.MyImage'
    IMAGESTORE_ALBUM_MODEL = 'mystoreapp.MyAlbum'

You should set form-related settings as string with python path to required class. For example::

    IMAGESTORE_IMAGE_FORM = 'mystoreapp.forms.MyImageForm'
    IMAGESTORE_ALBUM_FORM = 'mystoreapp.forms.MyAlbumForm'

Internally imagestore uses `django-swappable-models <https://github.com/wq/django-swappable-models>`_ reusable app.
So you can read ther docs to know how to use it correctly.

Warning
-------

* It is required to add app_label to your Image and Album models.
* Migrations with swappable models tested only with django migrations. Use it with south with caution.


Migrating from old versions (before 2.9.0)
------------------------------------------

* Before imagestore v.2.9.0 you have to set model-related settings to full python path to model class.
  Now it should be in ``app_label.model_class`` form.
* As now imagestore uses ``django-swappable-models`` app for swapping ``Album`` and ``Image`` models you should
  use swapper's methods for importing or referencing to imagestore models.
  For more info look at `django-swappable-models docs <https://github.com/wq/django-swappable-models/blob/master/README.md>`_