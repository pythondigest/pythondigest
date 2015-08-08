# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('digest', '0023_item_to_update'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parsingrules',
            name='if_element',
            field=models.CharField(choices=[('title', 'Заголовок новости'), ('link', 'Url новости'), ('content', 'Текст новости'), ('description', 'Описание новости'), ('http_code', 'HTTP Code')], verbose_name='Элемент условия', max_length=255, default='item_title'),
        ),
    ]
