# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [

        migrations.CreateModel(
            name='Tip',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('text', models.TextField(verbose_name='Совет')),
                ('active', models.BooleanField(default=True, verbose_name='Активен')),
            ],
            options={
                'verbose_name_plural': 'Рекомендации',
                'verbose_name': 'Рекомендация',
            },
        ),

    ]
