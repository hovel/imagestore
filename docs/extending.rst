Extending Imagestore
====================

You can extend imagestore by customizing Image and Album classes
as well as forms for their creation. Basic abstract classes that
I require to extend exists in `models.bases.image` and `models.bases.album`.

After you create your classes, tell imagestore to use them by setting next settings:

* IMAGESTORE_IMAGE_MODEL
* IMAGESTORE_ALBUM_MODEL
* IMAGESTORE_IMAGE_FORM
* IMAGESTORE_ALBUM_FORM


You should set settings as string with python path to required class. For example::

    IMAGESTORE_IMAGE_MODEL = 'image.models.Image'

Warning
-------

It is required to add app_label to your Image and Album models.