# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='JobFeed',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True,
                                        serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255,
                                          verbose_name='Название источника')),
                (
                'link', models.URLField(max_length=255, verbose_name='Ссылка')),
                ('incl', models.CharField(max_length=255, blank=True,
                                          help_text='Условие отбора новостей <br />                    Включение вида [text] <br />                    Включение при выводе будет удалено',
                                          null=True,
                                          verbose_name='Обязательное содержание')),
                ('excl', models.TextField(blank=True,
                                          help_text='Список источников подлежащих исключению через ", "',
                                          null=True,
                                          verbose_name='Список исключений')),
                ('in_edit', models.BooleanField(default=False,
                                                verbose_name='На тестировании')),
            ],
            options={
                'verbose_name': 'Источник импорта вакансий',
                'verbose_name_plural': 'Источники импорта вакансий',
            },
        ),
    ]
