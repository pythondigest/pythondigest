# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('digest', '0029_auto_20150825_1202'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='additionally',
            field=models.CharField(verbose_name='Дополнительно', null=True,
                                   max_length=255, blank=True),
        ),
    ]
