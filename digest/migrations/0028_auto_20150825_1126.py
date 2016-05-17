# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('digest', '0027_parsingrules_weight'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='activated_at',
            field=models.DateField(default=datetime.datetime.now,
                                   verbose_name='Дата активации'),
        ),
        migrations.AlterField(
            model_name='item',
            name='status',
            field=models.CharField(max_length=10,
                                   choices=[('pending', 'На рассмотрении'),
                                            ('active', 'Активная'),
                                            ('draft', 'Черновик'),
                                            ('moderated', 'Рассмотрена'),
                                            ('autoimport', 'Автоимпорт'),
                                            ('queue', 'В очереди')],
                                   default='pending', verbose_name='Статус'),
        ),
    ]
