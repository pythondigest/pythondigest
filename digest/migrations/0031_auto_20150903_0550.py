# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('digest', '0030_item_additionally'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='parsingrules',
            options={'ordering': ['-weight'], 'verbose_name': 'Правило обработки', 'verbose_name_plural': 'Правила обработки'},
        ),
    ]
