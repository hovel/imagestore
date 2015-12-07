# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import swapper


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '__first__'),
        swapper.dependency('imagestore', 'Album'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImagestoreAlbumCarousel',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('skin', models.CharField(default='jcarousel-skin-tango', max_length=100, verbose_name='Skin')),
                ('limit', models.IntegerField(null=True, verbose_name='Image limit', blank=True)),
                ('size', models.CharField(default='72x72', max_length=20, verbose_name='Thumbnail size')),
                ('full_size', models.CharField(default='600x600', max_length=20, verbose_name='Full size view')),
                ('template_file', models.CharField(default='cms/plugins/imagestore_album_carousel.html', max_length=100, null=True, verbose_name='Template file', blank=True)),
                ('album', models.ForeignKey(verbose_name='Album', to=swapper.get_model_name('imagestore', 'Album'))),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='ImagestoreAlbumPtr',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('album', models.ForeignKey(verbose_name='Album', to=swapper.get_model_name('imagestore', 'Album'))),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
    ]
