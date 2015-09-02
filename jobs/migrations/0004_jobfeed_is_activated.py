# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0003_auto_20150901_1242'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobfeed',
            name='is_activated',
            field=models.BooleanField(verbose_name='Включено', default=True),
        ),
    ]
