# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [('digest', '0005_auto_20150113_0900'), ]

    operations = [migrations.AlterField(
        model_name='item',
        name='modified_at',
        field=models.DateTimeField(
            null=True,
            verbose_name='\u0414\u0430\u0442\u0430 \u0438\u0437\u043c\u0435\u043d\u0435\u043d\u0438\u044f',
            blank=True), ), ]
