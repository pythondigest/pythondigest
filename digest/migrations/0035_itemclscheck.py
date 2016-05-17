# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('digest', '0034_item_article_path'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemClsCheck',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False,
                                        primary_key=True, auto_created=True)),
                ('last_check',
                 models.DateTimeField(verbose_name='Время последней проверки',
                                      auto_now=True)),
                ('status',
                 models.BooleanField(verbose_name='Оценка', default=False)),
                ('item', models.OneToOneField(to='digest.Item',
                                              verbose_name='Новость')),
            ],
        ),
    ]
