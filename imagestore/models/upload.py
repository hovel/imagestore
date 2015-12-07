# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import collections
import logging
import logging.config
import zipfile
import chardet
import swapper
from io import BytesIO
from PIL import Image as PILImage
from importlib import import_module
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.db import models
from django.utils.translation import ugettext_lazy as _

logger = logging.getLogger(__name__)

TEMP_DIR = getattr(settings, 'TEMP_DIR', 'temp/')


def process_zipfile(uploaded_album):
    Image = swapper.load_model('imagestore', 'Image')
    Album = swapper.load_model('imagestore', 'Album')

    if default_storage.exists(uploaded_album.zip_file.name):
        # TODO: implement try-except here
        zip = zipfile.ZipFile(uploaded_album.zip_file)
        bad_file = zip.testzip()
        if bad_file:
            raise Exception('"%s" in the .zip archive is corrupt.' % bad_file)

        if not uploaded_album.album:
            uploaded_album.album = \
                Album.objects.create(name=uploaded_album.new_album_name)

        for filename in sorted(zip.namelist()):
            try:
                encoding = chardet.detect(filename)['encoding']
                unicode_filename = filename.decode(encoding)
            except ValueError:  # if detect takes unicode string
                unicode_filename = filename

            # do not process meta files
            if unicode_filename.startswith('__'):
                continue

            logger.info('Processing file {}.'.format(unicode_filename))

            data = zip.read(filename)
            if len(data):
                try:
                    # the following is taken from django.forms.fields.ImageField:
                    # load() could spot a truncated JPEG, but it loads the entire
                    # image in memory, which is a DoS vector. See #3848 and #18520.
                    # verify() must be called immediately after the constructor.
                    PILImage.open(BytesIO(data)).verify()
                except Exception as e:
                    # if a "bad" file is found we just skip it.
                    logger.info('Error verify image: %s' % e)
                    continue

                if hasattr(data, 'seek') and \
                        isinstance(data.seek, collections.Callable):
                    logger.info('Seeked')
                    data.seek(0)

                try:
                    img = Image(album=uploaded_album.album)
                    img.image.save(filename, ContentFile(data))
                    img.save()
                except Exception as e:
                    logger.info('Error create Image: %s' % e)
                    continue
        zip.close()
        uploaded_album.delete()


upload_processor_function = \
    getattr(settings, 'IMAGESTORE_UPLOAD_ALBUM_PROCESSOR', None)
upload_processor = process_zipfile
if upload_processor_function:
    i = upload_processor_function.rfind('.')
    module = upload_processor_function[:i]
    attr = upload_processor_function[i + 1:]
    try:
        mod = import_module(module)
    except ImportError as e:
        raise ImproperlyConfigured('Error importing request processor module '
                                   '%s: "%s"' % (module, e))
    try:
        upload_processor = getattr(mod, attr)
    except AttributeError:
        raise ImproperlyConfigured('Module "%s" does not define a "%s" callable '
                                   'request processor' % (module, attr))


class AlbumUpload(models.Model):
    zip_file = models.FileField(
        verbose_name=_('images file (.zip)'), upload_to=TEMP_DIR,
        help_text=_('Select a .zip file of images to upload into a new Gallery.'))
    album = models.ForeignKey(
        swapper.get_model_name('imagestore', 'Album'),
        on_delete=models.CASCADE, blank=True, null=True,
        help_text=_('Select an album to add these images to. leave this empty '
                    'to create a new album from the supplied title.'))
    new_album_name = models.CharField(
        verbose_name=_('New album name'), max_length=255, blank=True,
        help_text=_('If not empty new album with this name will be created '
                    'and images will be upload to this album'))
    tags = models.CharField(verbose_name=_('tags'), max_length=255, blank=True)

    class Meta:
        app_label = 'imagestore'
        verbose_name = _('Album upload')
        verbose_name_plural = _('Album uploads')

    def save(self, *args, **kwargs):
        super(AlbumUpload, self).save(*args, **kwargs)
        upload_processor(self)

    def delete(self, *args, **kwargs):
        storage, path = self.zip_file.storage, self.zip_file.name
        super(AlbumUpload, self).delete(*args, **kwargs)
        storage.delete(path)
