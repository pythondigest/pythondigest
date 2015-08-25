# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('digest', '0028_auto_20150825_1126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='activated_at',
            field=models.DateTimeField(verbose_name='Дата активации', default=datetime.datetime.now),
        ),
    ]
