# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [('digest', '0022_auto_20150806_0905'), ]

    operations = [migrations.AddField(
        model_name='item',
        name='to_update',
        field=models.BooleanField(verbose_name='Обновить новость',
                                  default=False), ), ]
