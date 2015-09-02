# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0005_auto_20150902_0600'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jobitem',
            name='employer_name',
        ),
        migrations.RemoveField(
            model_name='jobitem',
            name='place',
        ),
    ]
