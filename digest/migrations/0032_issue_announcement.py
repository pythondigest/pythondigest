# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('digest', '0031_auto_20150903_0550'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='announcement',
            field=models.TextField(blank=True, null=True, verbose_name='Анонс'),
        ),
    ]
