# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [('digest', '0016_auto_20150731_1457'), ]

    operations = [migrations.AddField(
        model_name='parsingrules',
        name='is_activated',
        field=models.BooleanField(
            default=True,
            verbose_name='\u0412\u043a\u043b\u044e\u0447\u0435\u043d\u043e'), ),
    ]
