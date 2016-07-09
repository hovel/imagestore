# coding=utf-8
from __future__ import unicode_literals
from autocomplete_light import shortcuts as autocomplete_light
from tagging.models import Tag

autocomplete_light.register(
    Tag,
    search_fields=['^name']
)
