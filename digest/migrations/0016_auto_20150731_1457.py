# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [('digest', '0015_auto_20150731_0859'), ]

    operations = [
        migrations.AlterField(
            model_name='parsingrules',
            name='then_action',
            field=models.CharField(
                default=b'item_title',
                max_length=255,
                verbose_name='\u0414\u0435\u0439\u0441\u0442\u0432\u0438\u0435',
                choices=[(
                    b'set',
                    '\u0423\u0441\u0442\u0430\u043d\u043e\u0432\u0438\u0442\u044c'
                ), (b'add',
                    '\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c')]), ),
        migrations.AlterField(
            model_name='parsingrules',
            name='then_element',
            field=models.CharField(
                default=b'item_title',
                max_length=255,
                verbose_name='\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u0434\u0435\u0439\u0441\u0442\u0432\u0438\u044f',
                choices=[(b'section', '\u0420\u0430\u0437\u0434\u0435\u043b'), (
                    b'status', '\u0421\u0442\u0430\u0442\u0443\u0441'), (
                             b'tags',
                             '\u0422\u044d\u0433 \u043d\u043e\u0432\u043e\u0441\u0442\u0438'
                         )]), ),
    ]
