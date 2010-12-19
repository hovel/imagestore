import uuid
import os

from django.db import models
from django.db.models import permalink
from django.contrib.auth.models import User
from tagging.fields import TagField
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from sorl.thumbnail import ImageField
from mptt.models import MPTTModel


UPLOAD_TO = getattr(settings, 'IMAGESTORE_UPLOAD_TO', 'imagestore/')

#noinspection PyUnusedLocal
def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join(UPLOAD_TO, filename)

class Category(MPTTModel):
    class Meta(object):
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        ordering = ('order', 'title')

    parent = models.ForeignKey('self', blank=True, null=True, related_name='children')
    slug = models.SlugField(_('Slug'), max_length=200, blank=False, null=False)
    title = models.CharField(_('Title'), max_length=200, blank=False, null=False)
    order = models.IntegerField(_('Order'), null=False, blank=False)
    is_public = models.BooleanField(_('Is public'), default=False)

    def __unicode__(self):
        return self.title

    @permalink
    def get_absolute_url(self):
        return 'imagestore-category', (), {'slug': self.slug}

class Image(models.Model):
    class Meta(object):
        verbose_name = _('Image')
        verbose_name_plural = _('Images')
        ordering = ('order', 'id')

    title = models.CharField(_('Title'), max_length=200, blank=True, null=True)
    description = models.TextField(_('Description'), blank=True, null=True)
    tags = TagField(_('Tags'), blank=True)
    category = models.ForeignKey('Category', verbose_name=_('Category'), null=False, blank=False, related_name='images' )
    order = models.IntegerField(_('Order'), null=False, blank=False, default=0)
    is_public = models.BooleanField(_('Is public'), default=True)
    image = ImageField(verbose_name = _('Image'), upload_to=get_file_path)
    user = models.ForeignKey(User, verbose_name=_('User'), null=True, blank=True, related_name='images')

    @permalink
    def get_absolute_url(self):
        return 'imagestore-image', (), {'id': self.id}

    def __unicode__(self):
        return self.title

