# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0004_jobfeed_is_activated'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jobitem',
            name='salary_currency',
        ),
        migrations.RemoveField(
            model_name='jobitem',
            name='salary_from',
        ),
        migrations.RemoveField(
            model_name='jobitem',
            name='salary_till',
        ),
        migrations.RemoveField(
            model_name='jobitem',
            name='url_api',
        ),
        migrations.RemoveField(
            model_name='jobitem',
            name='url_logo',
        ),
        migrations.AddField(
            model_name='jobitem',
            name='description',
            field=models.TextField(null=True, blank=True, verbose_name='Описание вакансии'),
        ),
        migrations.AlterField(
            model_name='jobitem',
            name='employer_name',
            field=models.CharField(null=True, max_length=255, blank=True, verbose_name='Работодатель'),
        ),
        migrations.AlterField(
            model_name='jobitem',
            name='place',
            field=models.CharField(null=True, max_length=255, blank=True, verbose_name='Место'),
        ),
    ]
