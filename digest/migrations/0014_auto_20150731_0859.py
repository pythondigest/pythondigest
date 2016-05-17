# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [('digest', '0013_auto_20150730_1613'), ]

    operations = [migrations.CreateModel(
        name='Tag',
        fields=[('id', models.AutoField(verbose_name='ID',
                                        serialize=False,
                                        auto_created=True,
                                        primary_key=True)),
                ('name', models.CharField(
                    max_length=255,
                    verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 \u0442\u044d\u0433\u0430')
                 ), ],
        options={
            'verbose_name':
                '\u0422\u044d\u0433 \u043a \u043d\u043e\u0432\u043e\u0441\u0442\u0438',
            'verbose_name_plural':
                '\u0422\u044d\u0433\u0438 \u043a \u043d\u043e\u0432\u043e\u0441\u0442\u044f\u043c',
        }, ),
        migrations.AddField(
            model_name='item',
            name='tags',
            field=models.ManyToManyField(to='digest.Tag',
                                         null=True,
                                         verbose_name='\u0422\u044d\u0433\u0438',
                                         blank=True), ), ]
