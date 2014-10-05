#!/usr/bin/env python
# vim:fileencoding=utf-8

__author__ = 'zeus'


from django.db import models
from django.db.models import permalink
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from sorl.thumbnail import get_thumbnail
import logging

logger = logging.getLogger(__name__)

try:
    import Image as PILImage
except ImportError:
    from PIL import Image as PILImage

from imagestore.utils import get_model_string


SELF_MANAGE = getattr(settings, 'IMAGESTORE_SELF_MANAGE', True)


class BaseAlbum(models.Model):
    class Meta(object):
        abstract = True
        ordering = ('order', 'created', 'name')
        permissions = (
            ('moderate_albums', 'View, update and delete any album'),
        )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('User'), null=True, blank=True, related_name='albums')
    name = models.CharField(_('Name'), max_length=100, blank=False, null=False)
    brief = models.CharField(_('Brief'), max_length=255, blank=True, default='', help_text=_('Short description'))
    created = models.DateTimeField(_('Created'), auto_now_add=True)
    updated = models.DateTimeField(_('Updated'), auto_now=True)
    is_public = models.BooleanField(_('Is public'), default=True)
    head = models.ForeignKey(get_model_string('Image'), verbose_name=_('Head'), related_name='head_of', null=True, blank=True, on_delete=models.SET_NULL)

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
                logger.exception('IOError for album %s', img.image)
                return 'IOError'
        return _('Empty album')

    admin_thumbnail.short_description = _('Head')
    admin_thumbnail.allow_tags = True
