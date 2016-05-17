# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('jobs', '0002_jobitem'),
    ]

    operations = [
        migrations.CreateModel(
            name='AcceptedList',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID',
                                        primary_key=True, serialize=False)),
                ('title',
                 models.CharField(max_length=255, verbose_name='Строка')),
            ],
            options={
                'verbose_name': 'Слисок одобрения',
                'verbose_name_plural': 'Строки для одобрения',
            },
        ),
        migrations.CreateModel(
            name='RejectedList',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID',
                                        primary_key=True, serialize=False)),
                ('title',
                 models.CharField(max_length=255, verbose_name='Строка')),
            ],
            options={
                'verbose_name': 'Слисок исключения',
                'verbose_name_plural': 'Строки для исключения',
            },
        ),
        migrations.RemoveField(
            model_name='jobfeed',
            name='excl',
        ),
        migrations.RemoveField(
            model_name='jobfeed',
            name='incl',
        ),
    ]
