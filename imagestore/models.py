from django.db import models
from django.db.models import permalink
from tagging.fields import TagField
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from sorl.thumbnail import ImageField
from mptt.models import MPTTModel



UPLOAD_TO = getattr(settings, 'IMAGESTORE_UPLOAD_TO', 'imagestore/')


class Category(MPTTModel):
    class Meta(object):
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    parent = models.ForeignKey('self', blank=True, null=True, related_name='children')
    slug = models.SlugField(_('Slug'), max_length=200, blank=False, null=False)
    title = models.CharField(_('Title'), max_length=200, blank=False, null=False)
    order = models.IntegerField(_('Order'), null=False)
    is_public = models.BooleanField(_('Is public'), default=False)

    def __unicode__(self):
        return self.title

    @permalink
    def get_absolute_url(self):
        return ('imagestore-category', (), {'slug': self.slug})

class Image(models.Model):
    class Meta(object):
        verbose_name = _('Image')
        verbose_name_plural = _('Images')

    slug = models.SlugField(_('Slug'), max_length=200, blank=True, null=True)
    title = models.CharField(_('Title'), max_length=200, blank=True, null=True)
    description = models.TextField(_('Description'), blank=True, null=True)
    tags = TagField(_('Tags'), blank=True)
    category = models.ForeignKey('Category', null=False, blank=False, verbose_name=_('Category'))
    order = models.IntegerField(_('Order'), null=True, blank=True)
    is_public = models.BooleanField(_('Is public'), default=True)
    image = ImageField(verbose_name = _('Image'), upload_to=UPLOAD_TO)

    @permalink
    def get_absolute_url(self):
        return ('imagestore-image', (), {'slug_or_id': self.id})

    def __unicode__(self):
        return self.title

