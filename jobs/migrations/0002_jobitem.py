# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('jobs', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobItem',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False,
                                        primary_key=True, verbose_name='ID')),
                ('title',
                 models.CharField(max_length=255, verbose_name='Название')),
                ('employer_name',
                 models.CharField(max_length=255, verbose_name='Работодатель')),
                ('place',
                 models.CharField(max_length=255, verbose_name='Место')),
                ('link', models.URLField(verbose_name='Ссылка')),
                ('salary_from',
                 models.PositiveIntegerField(null=True, blank=True,
                                             verbose_name='Заработная плата')),
                ('salary_till',
                 models.PositiveIntegerField(null=True, blank=True,
                                             verbose_name='З/п до')),
                ('salary_currency',
                 models.CharField(null=True, max_length=255, blank=True,
                                  verbose_name='Валюта')),
                ('url_api', models.URLField(null=True, blank=True,
                                            verbose_name='URL API')),
                ('url_logo', models.URLField(null=True, blank=True,
                                             verbose_name='URL логотипа')),
            ],
            options={
                'verbose_name_plural': 'Работа',
                'verbose_name': 'Вакансия',
            },
        ),
    ]
