# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imagestore', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='album',
            name='brief',
            field=models.CharField(default='', help_text='Short description', max_length=255, verbose_name='Brief', blank=True),
        ),
    ]
