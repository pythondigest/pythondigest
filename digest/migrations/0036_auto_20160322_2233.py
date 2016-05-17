# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('digest', '0035_itemclscheck'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='itemclscheck',
            options={'verbose_name': 'Проверка классификатором',
                     'verbose_name_plural': 'Проверка классификатором'},
        ),
    ]
