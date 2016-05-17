# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('digest', '0032_issue_announcement'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemDailyModerator',
            fields=[
            ],
            options={
                'verbose_name_plural': 'Новости (разметка дневного дайджеста)',
                'proxy': True,
            },
            bases=('digest.item',),
        ),
        migrations.AddField(
            model_name='issue',
            name='trend',
            field=models.CharField(blank=True, verbose_name='Тенденция недели',
                                   null=True, max_length=255),
        ),
    ]
