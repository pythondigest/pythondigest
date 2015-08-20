# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [('digest', '0009_autoimportresource_language'), ]

    operations = [migrations.CreateModel(
        name='ParsingRules',
        fields=[('id', models.AutoField(verbose_name='ID',
                                        serialize=False,
                                        auto_created=True,
                                        primary_key=True)),
                ('name', models.CharField(
                    max_length=255,
                    verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 \u043f\u0440\u0430\u0432\u0438\u043b\u0430')
                 ),
                ('if_element', models.CharField(
                    default=b'item_title',
                    max_length=255,
                    verbose_name='\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u0443\u0441\u043b\u043e\u0432\u0438\u044f',
                    choices=[(
                        b'item_title',
                        '\u0417\u0430\u0433\u043e\u043b\u043e\u0432\u043e\u043a \u043d\u043e\u0432\u043e\u0441\u0442\u0438'
                    ), (b'item_url', 'Url \u043d\u043e\u0432\u043e\u0441\u0442\u0438'), (
                        b'item_content',
                        '\u0422\u0435\u043a\u0441\u0442 \u043d\u043e\u0432\u043e\u0441\u0442\u0438'
                    ), (b'http_code', 'HTTP Code')])),
                ('if_action', models.CharField(
                    default=b'consist',
                    max_length=255,
                    verbose_name='\u0423\u0441\u043b\u043e\u0432\u0438\u0435',
                    choices=[(b'equal', '\u0420\u0430\u0432\u0435\u043d'), (
                        b'consist', '\u0421\u043e\u0434\u0435\u0440\u0436\u0438\u0442'
                    ), (b'not_equal', '\u041d\u0435 \u0440\u0430\u0432\u0435\u043d')])),
                ('if_value', models.CharField(
                    max_length=255,
                    verbose_name='\u0417\u043d\u0430\u0447\u0435\u043d\u0438\u0435')),
                ('then_element', models.CharField(
                    default=b'item_title',
                    max_length=255,
                    verbose_name='\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u0434\u0435\u0439\u0441\u0442\u0432\u0438\u044f',
                    choices=[(
                        b'item_title',
                        '\u0417\u0430\u0433\u043e\u043b\u043e\u0432\u043e\u043a \u043d\u043e\u0432\u043e\u0441\u0442\u0438'
                    ), (b'item_url', 'Url \u043d\u043e\u0432\u043e\u0441\u0442\u0438'), (
                        b'item_content',
                        '\u0422\u0435\u043a\u0441\u0442 \u043d\u043e\u0432\u043e\u0441\u0442\u0438'
                    ), (b'http_code', 'HTTP Code')])),
                ('then_action', models.CharField(
                    default=b'item_title',
                    max_length=255,
                    verbose_name='\u0414\u0435\u0439\u0441\u0442\u0432\u0438\u0435',
                    choices=[(
                        b'item_title',
                        '\u0417\u0430\u0433\u043e\u043b\u043e\u0432\u043e\u043a \u043d\u043e\u0432\u043e\u0441\u0442\u0438'
                    ), (b'item_url', 'Url \u043d\u043e\u0432\u043e\u0441\u0442\u0438'), (
                        b'item_content',
                        '\u0422\u0435\u043a\u0441\u0442 \u043d\u043e\u0432\u043e\u0441\u0442\u0438'
                    ), (b'http_code', 'HTTP Code')])),
                ('then_value', models.CharField(
                    max_length=255,
                    verbose_name='\u0417\u043d\u0430\u0447\u0435\u043d\u0438\u0435')), ],
        options={
            'verbose_name':
            '\u041f\u0440\u0430\u0432\u0438\u043b\u043e \u043e\u0431\u0440\u0430\u0431\u043e\u0442\u043a\u0438',
            'verbose_name_plural':
            '\u041f\u0440\u0430\u0432\u0438\u043b\u0430 \u043e\u0431\u0440\u0430\u0431\u043e\u0442\u043a\u0438',
        }, ),
        migrations.AlterField(
        model_name='item',
        name='related_to_date',
        field=models.DateField(
            default=datetime.datetime.today,
            help_text='\u041d\u0430\u043f\u0440\u0438\u043c\u0435\u0440, \u0434\u0430\u0442\u0430 \u043f\u0443\u0431\u043b\u0438\u043a\u0430\u0446\u0438\u0438 \u043d\u043e\u0432\u043e\u0441\u0442\u0438 \u043d\u0430 \u0438\u0441\u0442\u043e\u0447\u043d\u0438\u043a\u0435',
            verbose_name='\u0414\u0430\u0442\u0430'), ), ]
