Extending Imagestore
====================

The extension mechanism
-----------------------------
Imagestore features an extension mechanism which enables you to add
custom fields to ``Image`` and ``Album`` models without modifying
its core. The steps to extend imagestore are:

#. Create a new app that will contain the customized models.
#. Create your customized models by extending the basic abstract classes ``models.bases.image`` and ``models.bases.album`` which are provided by imagestore.
#. Add the app containing your custom classes to the list of ``INSTALLED_APPS``.
#. Use the ``IMAGESTORE_IMAGE_FORM`` and ``IMAGESTORE_IMAGE_FORM`` :ref:`settings <settings-label>` to tell imagestore to use your classes.
#. Sync database schema (``syncdb``).

You can also customize the forms used by imagestore for creating
new ``Image`` and ``Album`` instances. This is done by using
the ``IMAGESTORE_IMAGE_FORM`` and ``IMAGESTORE_ALBUM_FORM``
:ref:`settings <settings-label>` to tell imagestore which forms should
be used.


.. _extending-tips-label:

Catches and Tips
----------------
.. highlight:: python

* You should properly set the properties of the ``Meta`` inner-class of your custom models::

    from imagestore.models.bases.image import BaseImage

    class MyImage(BaseImage):
        class Meta(BaseImage.Meta):
            abstract = False   # make class non-abstract
            app_label = 'imagestore'   # tell django that this model actually belongs to the imagestore app
            db_table = 'imagestore_image'  # use an alternate database table (optional)
            ...
    
        extra_field1 = ...
        extra_field2 = ...

* You should set your custom classes as strings in your settings file::

    IMAGESTORE_IMAGE_MODEL = 'myimagestore.models.MyImage'

* You will need a new admin class for your custom model in order to have it appear in the django admin.
  You can use inheritance to extend the existing admin class::

    from django.contrib import admin
    import imagestore.admin
    import models

    class MyImageAdmin(imagestore.admin.ImageAdmin):
        def __init__(self, *args, **kwargs):
            self.fieldsets += (('Extra fields', {'fields': ['extra_field1', 'extra_field2']}),)
            super(MyImageAdmin, self).__init__(*args, **kwargs)

    admin.site.register(models.MyImage, MyImageAdmin)


Extending an existing imagestore gallery
----------------------------------------
As one could easily guess, customizing imagestore means that changes
will be made to the underlying database schema. Such changes are not
trivial to handle while keeping your data at the same time.
Following, we highlight how one can handle customization of an existing
imagestore installation.

Using plain Django
~~~~~~~~~~~~~~~~~~
The Django core currently does not provide any mechanism to handle changes
to the database schema. You can only drop database tables and create them 
from scratch. Repopulating the new tables with the old data should be done
manually. Fortunately, Django does provide some tools to make this easier
for you.

.. highlight:: bash

* **Adding optional fields / fields with default values**:
  In order to make a field in your model optional, you set the ``blank`` and ``null``
  `field options <https://docs.djangoproject.com/en/dev/ref/models/fields/#field-options>`_
  to `True`. E.g. ``extra_field1 = models.IntegerField(blank=True, null=True)``.
  
  If all the fields you add to your custom imagestore models are optionali or have
  a default value set, it is pretty straightforward to move your data to the new schema::

    # keep backup of the imagestore data
    $ ./manage.py dumpdata imagestore --indent=2 > imagestore-backup.json

    # remove tables of the old schema
    $ ./manage.py sqlclear imagestore | ./manage.py dbshell

    # create tables with the new schema
    $ ./manage.py syncdb

    # restore data 
    $ ./manage.py loaddata ./imagestore-backup.json
  
  This technique works because the value for the newly added field is either 
  optional or provided as a default. So, loading from the dump created with
  the old schema won't raise any integrity errors.

* **Adding mandatory fields**:
  Adding mandatory fields (without default values set) to an imagestore model
  and keeping your data is much more complex.
  One option to achieve it would be to use the ``db_table`` ``Meta`` class
  property (see :ref:`above <extending-tips-label>`) so that your custom model
  uses an alternate database table.
  
  This will leave your original database table unaltered after running ``syncdb``.
  At this point you can use your database shell (``./manage.py dbshell``) to
  manually copy the data from the original table to the new one.
  Filler values should be provided for the mandatory fields.
  After copying the data, you can remove the ``db_table`` ``Meta`` property, drop
  the old table and rename the new one.

Using South
~~~~~~~~~~~
`Django South <http://south.aeracode.org/docs/>`_ is a Django
application which aims to make changing your application models
relatively painless. South alters the database schema (tables,
columns etc.) and brings it up to date with the app models without
having to start from scratch.
Imagestore already uses South to manage changes in its models.

Extending imagestore when using South is slightly tricky. This is
because we essentially make changes to the imagestore models, yet
we want the migrations for these changes to live under a different
application codebase (i.e. the codebase of the app that holds our
custom models).

.. highlight:: bash

* **Initial migration**:
  We can "trick" South to automatically generate the initial 
  migration for our custom app. To detect the changes, the ``schemamigration``
  south command should be run against the imagestore applications.
  The produced code should be redirected and stored as a migration
  of our custom app (let's call it ``imagestore_custom``)::

    # bootstrap migrations dir
    # the migration will essentially do nothing - all classes in models.py marked belonging to imagestore
    $ ./manage.py schemamigration --initial imagestore_custom

    # overwrite custom app migration with the actual autogenerated imagestore migration 
    $ ./manage.py schemamigration --auto --stdout imagestore > imagestore_custom/migrations/0001_initial.py 

    # apply migration
    $ ./manage.py migrate imagestore_customizations

    # the migration has modified imagestore models, yet recorded as belonging to imagestore_custom
    $ echo 'select * from south_migrationhistory order by applied desc limit 10;' | ./manage.py dbshell

* **Subsequent migrations**:
  For further changes to our custom models, automatically detection
  of changes by South (``--auto`` option) doesn't work. This is
  because during the change detection process, South won't take
  into account any changes made in migrations not living under the
  imagestore codebase. As a result, the migration that will be
  produced will attempt to create fields that already exist.

  One option here is to manually edit the automatically produced
  migration to fix this. Another option is to manually tell South
  what change(s) to include in the migration::

    $ ./manage.py schemamigration --add-field=Image.extra_field3 --stdout imagestore > imagestore_custom/migrations/0002__add_field_image_extra_field3.py
     ? The field 'Image.extra_field3' does not have a default specified, yet is NOT NULL.
     ? Since you are adding this field, you MUST specify a default
     ? value to use for existing rows. Would you like to:
     ? 1. Quit now, and add a default to the field in models.py
     ? 2. Specify a one-off value to use for existing columns now
     ? Please select a choice: 2
     ? Please enter Python code for your one-off default value.
     ? The datetime module is available, so you can do e.g. datetime.date.today()
     >>> 42
     + Added field extra_field3 on imagestore.Image
    $

* **Mandatory field handling**: As one can see in the previous example, when a mandatory
  field with no default value is added to a model (e.g. ``extra_field3``), South will prompt
  you for a default value when creating the ``schemamigration``. The default values set
  can later be fixed by creating a South ``datamigration``.


