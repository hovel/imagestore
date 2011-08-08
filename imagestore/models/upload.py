#!/usr/bin/env python
# vim:fileencoding=utf-8

__author__ = 'zeus'

import os
import zipfile
from django.db import models
from imagestore.utils import load_class, get_model_string
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.core.files.base import ContentFile
try:
    import Image as PILImage
except ImportError:
    from PIL import Image as PILImage

from imagestore.models import Album, Image

TEMP_DIR = getattr(settings, 'TEMP_DIR', 'temp/')

class AlbumUpload(models.Model):
    """
    Just re-written django-photologue GalleryUpload method
    """
    zip_file = models.FileField(_('images file (.zip)'), upload_to=TEMP_DIR,
                                help_text=_('Select a .zip file of images to upload into a new Gallery.'))
    album = models.ForeignKey(
        Album,
        null=True,
        blank=True,
        help_text=_('Select an album to add these images to. leave this empty to create a new album from the supplied title.')
    )
    new_album_name = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_('New album name'),
        help_text=_('If not empty new album with this name will be created and images will be upload to this album')
        )
    tags = models.CharField(max_length=255, blank=True, verbose_name=_('tags'))

    class Meta(object):
        verbose_name = _('Album upload')
        verbose_name_plural = _('Album uploads')
        app_label = 'imagestore'

    def save(self, *args, **kwargs):
        super(AlbumUpload, self).save(*args, **kwargs)
        album = self.process_zipfile()
        super(AlbumUpload, self).delete()
        return album

    def process_zipfile(self):
        if os.path.isfile(self.zip_file.path):
            # TODO: implement try-except here
            zip = zipfile.ZipFile(self.zip_file.path)
            bad_file = zip.testzip()
            if bad_file:
                raise Exception('"%s" in the .zip archive is corrupt.' % bad_file)
            count = 1
            album = self.album
            if not album:
                album = Album.objects.create(name=self.new_album_name)
            from cStringIO import StringIO
            for filename in sorted(zip.namelist()):
                if filename.startswith('__'): # do not process meta files
                    continue
                data = zip.read(filename)
                if len(data):
                    try:
                        # the following is taken from django.newforms.fields.ImageField:
                        #  load() is the only method that can spot a truncated JPEG,
                        #  but it cannot be called sanely after verify()
                        trial_image = PILImage.open(StringIO(data))
                        trial_image.load()
                        # verify() is the only method that can spot a corrupt PNG,
                        #  but it must be called immediately after the constructor
                        trial_image = PILImage.open(StringIO(data))
                        trial_image.verify()
                    except Exception:
                        # if a "bad" file is found we just skip it.
                        continue
                    img = Image(album=album)
                    img.image.save(filename, ContentFile(data))
                    img.save()
            zip.close()
            return album
