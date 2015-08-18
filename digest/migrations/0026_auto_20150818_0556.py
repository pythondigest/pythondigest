# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('digest', '0025_auto_20150813_0925'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='status',
            field=models.CharField(default='pending', verbose_name='Статус', max_length=10, choices=[('pending', 'На рассмотрении'), ('active', 'Активная'), ('draft', 'Черновик'), ('moderated', 'Рассмотрена'), ('autoimport', 'Автоимпорт')]),
        ),
    ]
