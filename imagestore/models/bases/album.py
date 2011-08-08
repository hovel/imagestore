#!/usr/bin/env python
# vim:fileencoding=utf-8

__author__ = 'zeus'


from django.db import models
from django.db.models import permalink
from sorl.thumbnail.helpers import ThumbnailError
from tagging.fields import TagField
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from sorl.thumbnail import ImageField, get_thumbnail
from django.contrib.auth.models import User, Permission
from django.db.models.signals import post_save
try:
    import Image as PILImage
except ImportError:
    from PIL import Image as PILImage

from imagestore.utils import get_file_path, get_model_string



SELF_MANAGE = getattr(settings, 'IMAGESTORE_SELF_MANAGE', True)


class BaseAlbum(models.Model):
    class Meta(object):
        abstract = True
        ordering = ('created', 'name')
        permissions = (
            ('moderate_albums', 'View, update and delete any album'),
        )

    user = models.ForeignKey(User, verbose_name=_('User'), null=True, blank=True, related_name='albums')
    name = models.CharField(_('Name'), max_length=100, blank=False, null=False)
    created = models.DateTimeField(_('Created'), auto_now_add=True)
    updated = models.DateTimeField(_('Updated'), auto_now=True)
    is_public = models.BooleanField(_('Is public'), default=True)
    head = models.ForeignKey(get_model_string('Image'), related_name='head_of', null=True, blank=True)

    order = models.IntegerField(_('Order'), default=0)

    def get_head(self):
        if self.head:
            return self.head
        else:
            if self.images.all().count()>0:
                self.head = self.images.all()[0]
                self.save()
                return self.head
            else:
                return None

    @permalink
    def get_absolute_url(self):
        return 'imagestore:album', (), {'album_id': self.id}

    def __unicode__(self):
        return self.name

    def admin_thumbnail(self):
        img = self.get_head()
        if img:
            try:
                return '<img src="%s">' % get_thumbnail(img.image, '100x100', crop='center').url
            except IOError:
                return 'IOError'
        return _('Empty album')

    admin_thumbnail.short_description = _('Head')
    admin_thumbnail.allow_tags = True