# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('digest', '0011_auto_20150730_0556'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parsingrules',
            name='if_action',
            field=models.CharField(default=b'consist', max_length=255, verbose_name='\u0423\u0441\u043b\u043e\u0432\u0438\u0435', choices=[(b'equal', '\u0420\u0430\u0432\u0435\u043d'), (b'contains', '\u0421\u043e\u0434\u0435\u0440\u0436\u0438\u0442'), (b'not_equal', '\u041d\u0435 \u0440\u0430\u0432\u0435\u043d')]),
        ),
    ]
