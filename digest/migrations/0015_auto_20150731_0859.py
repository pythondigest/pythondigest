# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [('digest', '0014_auto_20150731_0859'), ]

    operations = [migrations.AlterField(
        model_name='item',
        name='tags',
        field=models.ManyToManyField(to='digest.Tag',
                                     verbose_name='\u0422\u044d\u0433\u0438',
                                     blank=True), ), ]
