# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [('digest', '0012_auto_20150730_0611'), ]

    operations = [
        migrations.AlterField(
            model_name='parsingrules',
            name='if_action',
            field=models.CharField(
                default=b'consist',
                max_length=255,
                verbose_name='\u0423\u0441\u043b\u043e\u0432\u0438\u0435',
                choices=[(b'equal', '\u0420\u0430\u0432\u0435\u043d'), (
                    b'contains',
                    '\u0421\u043e\u0434\u0435\u0440\u0436\u0438\u0442'
                ), (b'not_equal',
                    '\u041d\u0435 \u0440\u0430\u0432\u0435\u043d'),
                         (b'regex', 'Regex match')]), ),
        migrations.AlterField(
            model_name='parsingrules',
            name='if_element',
            field=models.CharField(
                default=b'item_title',
                max_length=255,
                verbose_name='\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u0443\u0441\u043b\u043e\u0432\u0438\u044f',
                choices=[(
                    b'item_title',
                    '\u0417\u0430\u0433\u043e\u043b\u043e\u0432\u043e\u043a \u043d\u043e\u0432\u043e\u0441\u0442\u0438'
                ), (b'item_url',
                    'Url \u043d\u043e\u0432\u043e\u0441\u0442\u0438'), (
                    b'item_content',
                    '\u0422\u0435\u043a\u0441\u0442 \u043d\u043e\u0432\u043e\u0441\u0442\u0438'
                ), (
                    b'item_description',
                    '\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435 \u043d\u043e\u0432\u043e\u0441\u0442\u0438'
                ), (b'http_code', 'HTTP Code')]), ),
    ]
