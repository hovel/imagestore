# coding=utf-8
from __future__ import unicode_literals
import autocomplete_light
from tagging.models import Tag

autocomplete_light.register(
    Tag,
    search_fields=['^name']
)