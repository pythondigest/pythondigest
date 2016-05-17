# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('digest', '0028_auto_20150825_1126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='activated_at',
            field=models.DateTimeField(verbose_name='Дата активации',
                                       default=datetime.datetime.now),
        ),
    ]
