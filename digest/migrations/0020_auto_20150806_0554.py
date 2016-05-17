# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [('digest', '0019_auto_20150805_1332'), ]

    operations = [migrations.AlterField(
        model_name='parsingrules',
        name='then_element',
        field=models.CharField(default='item_title',
                               verbose_name='Элемент действия',
                               max_length=255,
                               choices=[('title', 'Заголовок новости'), (
                                   'description', 'Описание новости'
                               ), ('section', 'Раздел'), ('status', 'Статус'),
                                        ('tags', 'Тэг новости')]), ), ]
