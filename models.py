from django.db import models
from tagging.fields import TagField
from tagging.models import Tag, TaggedItem
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.core.cache import cache
from persons.models import Person

import logging

class Category(models.Model):
    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    slug = models.SlugField(_('Slug'), max_length=200, blank=False, null=False)
    title = models.CharField(_('Title'), max_length=200, blank=False, null=False)

    def __unicode__(self):
        return self.title

class Image(models.Model):
    class Meta:
        verbose_name = _('Image')
        verbose_name_plural = _('Images')

    slug = models.SlugField(_('Slug'), max_length=200)
    title = models.CharField(_('Title'), max_length=200, blank=True, null=True)
    description = models.TextField(_('Description'), blank=True, null=True)
    tags = TagField(_('Tags'), blank=True)
    category = models.ForeignKey('Category', null=False, blank=False)
    author = models.ForeignKey(Person, null=False, blank=False)
    image = models.ImageField(upload_to='imagestore/')

    def __unicode__(self):
        return self.title


