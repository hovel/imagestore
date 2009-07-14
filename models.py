from django.db import models
from django.db.models import permalink
from tagging.fields import TagField
from tagging.models import Tag, TaggedItem
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.core.cache import cache
from persons.models import Person
from sorl.thumbnail.fields import ImageWithThumbnailsField


#import logging

UPLOAD_TO = 'imagestore/'


class Category(models.Model):
    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    slug = models.SlugField(_('Slug'), max_length=200, blank=False, null=False)
    title = models.CharField(_('Title'), max_length=200, blank=False, null=False)
    order = models.IntegerField(_('Order'), null=False)

    def __unicode__(self):
        return self.title

    @permalink
    def get_absolute_url(self):
        return ('imagestore-category', (), {'slug': self.slug})

class Image(models.Model):
    class Meta:
        verbose_name = _('Image')
        verbose_name_plural = _('Images')

    slug = models.SlugField(_('Slug'), max_length=200, blank=True, null=True)
    title = models.CharField(_('Title'), max_length=200, blank=True, null=True)
    description = models.TextField(_('Description'), blank=True, null=True)
    tags = TagField(_('Tags'), blank=True)
    category = models.ForeignKey('Category', null=False, blank=False, verbose_name=_('Category'))
    author = models.ForeignKey(Person, null=False, blank=False, verbose_name=_('Author'))
    order = models.IntegerField(_('Order'), null=False)
    image = ImageWithThumbnailsField(
        upload_to='imagestore',
        thumbnail={'size': (100, 100)},
        extra_thumbnails={
            'icon': {'size': (16, 16), 'options': ['crop', 'upscale'], 'extension': 'jpg'},
            'small': {'size': (70, 70), 'extension': 'jpg'},
            'preview': {'size': (120, 120), 'extension': 'jpg'},
            'display': {'size': (700, 900), 'extension': 'jpg'},
        },
    )

    @permalink
    def get_absolute_url(self):
        return ('imagestore-image', (), {'slug_or_id': self.id})

    def __unicode__(self):
        return self.title

