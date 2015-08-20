# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [('digest', '0017_parsingrules_is_activated'), ]

    operations = [migrations.CreateModel(
        name='Package',
        fields=[('id', models.AutoField(verbose_name='ID',
                                        serialize=False,
                                        auto_created=True,
                                        primary_key=True)),
                ('name', models.CharField(
                    max_length=255,
                    verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
                ('description', models.TextField(
                    null=True,
                    verbose_name='\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435',
                    blank=True)),
                ('url', models.CharField(max_length=255,
                                         verbose_name='\u0421\u0441\u044b\u043b\u043a\u0430')), ],
        options={
            'verbose_name':
            '\u0411\u0438\u0431\u043b\u0438\u043e\u0442\u0435\u043a\u0430',
            'verbose_name_plural':
            '\u0411\u0438\u0431\u043b\u0438\u043e\u0442\u0435\u043a\u0438',
        }, ), ]
