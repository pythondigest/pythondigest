# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0007_auto_20150902_0605'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobitem',
            name='employer_name',
            field=models.CharField(max_length=255, verbose_name='Работодатель', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='jobitem',
            name='published_at',
            field=models.DateTimeField(editable=False, verbose_name='Дата публикации', null=True),
        ),
        migrations.AddField(
            model_name='jobitem',
            name='salary_currency',
            field=models.CharField(max_length=255, verbose_name='Валюта', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='jobitem',
            name='salary_from',
            field=models.PositiveIntegerField(verbose_name='Заработная плата', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='jobitem',
            name='salary_till',
            field=models.PositiveIntegerField(verbose_name='З/п до', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='jobitem',
            name='src_id',
            field=models.CharField(max_length=50, verbose_name='ID в источнике', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='jobitem',
            name='src_place_id',
            field=models.CharField(max_length=20, db_index=True, verbose_name='ID места в источнике', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='jobitem',
            name='src_place_name',
            field=models.CharField(max_length=255, verbose_name='Название места в источнике', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='jobitem',
            name='url_api',
            field=models.URLField(verbose_name='URL API', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='jobitem',
            name='url_logo',
            field=models.URLField(verbose_name='URL логотипа', blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='jobitem',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата создания', null=True),
        ),
        migrations.AlterField(
            model_name='jobitem',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Дата обновления', null=True),
        ),
    ]
