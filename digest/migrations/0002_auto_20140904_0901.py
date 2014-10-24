# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('digest', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FilteringRule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('op', models.CharField(max_length=50, verbose_name='\u041e\u043f\u0435\u0440\u0430\u0446\u0438\u044f', choices=[(b'include', '\u0412\u043a\u043b\u044e\u0447\u0438\u0442\u044c \u0435\u0441\u043b\u0438'), (b'exclude', '\u041f\u0440\u043e\u043f\u0443\u0441\u0442\u0438\u0442\u044c \u0435\u0441\u043b\u0438')])),
                ('for_field', models.CharField(default=b'*', max_length=255, verbose_name='\u041f\u043e\u043b\u0435')),
                ('type', models.CharField(max_length=50, verbose_name='\u041f\u0440\u0430\u0432\u0438\u043b\u043e', choices=[(b'contains', '\u0421\u043e\u0434\u0435\u0440\u0436\u0438\u0442'), (b'startswith', '\u041d\u0430\u0447\u0438\u043d\u0430\u0435\u0442\u0441\u044f c'), (b'endswith', '\u0417\u0430\u043a\u0430\u043d\u0447\u0438\u0432\u0430\u0435\u0442\u0441\u044f'), (b'regex', '\u041f\u043e\u0434\u0445\u043e\u0434\u0438\u0442 \u043f\u043e regexp')])),
                ('value', models.CharField(max_length=255, verbose_name='\u0417\u043d\u0430\u0447\u0435\u043d\u0438\u0435')),
                ('resource', models.ForeignKey(verbose_name='\u0420\u0435\u0441\u0443\u0440\u0441', to='digest.AutoImportResource')),
            ],
            options={
                'verbose_name': '\u041f\u0440\u0430\u0432\u0438\u043b\u043e \u0434\u043b\u044f \u043e\u0431\u0440\u0430\u0431\u043e\u0442\u043a\u0438 \u0434\u0430\u043d\u043d\u044b\u0445',
                'verbose_name_plural': '\u041f\u0440\u0430\u0432\u0438\u043b\u0430 \u0434\u043b\u044f \u043e\u0431\u0440\u0430\u0431\u043e\u0442\u043a\u0438 \u0434\u0430\u043d\u043d\u044b\u0445',
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='autoimportresource',
            name='excl',
        ),
        migrations.RemoveField(
            model_name='autoimportresource',
            name='incl',
        ),
    ]
