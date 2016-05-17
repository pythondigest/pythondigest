# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [('frontend', '0002_auto_20150805_1801'),
                    ('digest', '0020_auto_20150806_0554'), ]

    operations = [
        migrations.AddField(model_name='issue',
                            name='tip',
                            field=models.ForeignKey(verbose_name='Совет',
                                                    null=True,
                                                    blank=True,
                                                    to='frontend.Tip'), ),
    ]
