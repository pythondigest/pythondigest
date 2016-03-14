# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('digest', '0033_auto_20160227_0923'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='article_path',
            field=models.FilePathField(blank=True, verbose_name='Путь до статьи', null=True),
        ),
    ]
