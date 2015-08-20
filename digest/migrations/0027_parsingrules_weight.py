# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [('digest', '0026_auto_20150818_0556'), ]

    operations = [migrations.AddField(
        model_name='parsingrules',
        name='weight',
        field=models.PositiveIntegerField(default=100,
                                          verbose_name='Weight'), ), ]
