# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [('digest', '0024_auto_20150808_0825'), ]

    operations = [
        migrations.CreateModel(
            name='ItemModerator',
            fields=[],
            options={'proxy': True,
                     'verbose_name_plural': 'Новости (эксперимент)',},
            bases=('digest.item',), ),
        migrations.AddField(model_name='issue',
                            name='last_item',
                            field=models.IntegerField(
                                verbose_name='Последняя модерированая новость',
                                null=True,
                                blank=True), ),
    ]
