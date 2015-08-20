# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [('digest', '0007_auto_20150405_1654'), ]

    operations = [migrations.AlterField(
        model_name='item',
        name='status',
        field=models.CharField(
            default=b'pending',
            max_length=10,
            verbose_name='\u0421\u0442\u0430\u0442\u0443\u0441',
            choices=[(
                b'pending',
                '\u041e\u0436\u0438\u0434\u0430\u0435\u0442 \u0440\u0430\u0441\u0441\u043c\u043e\u0442\u0440\u0435\u043d\u0438\u044f'
            ), (b'active', '\u0410\u043a\u0442\u0438\u0432\u043d\u0430\u044f'), (
                b'draft', '\u0427\u0435\u0440\u043d\u043e\u0432\u0438\u043a'), (
                    b'moderated',
                    '\u041e\u0442\u043c\u043e\u0434\u0435\u0440\u0438\u0440\u043e\u0432\u0430\u043d\u043e'
            ), (
                    b'autoimport', '\u0414\u043e\u0431\u0430\u0432\u043b\u0435\u043d\u0430 \u0430\u0432\u0442\u043e\u0438\u043c\u043f\u043e\u0440\u0442\u043e\u043c'
            )]), ), ]
