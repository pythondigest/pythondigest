# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.db.models.expressions import F
from digest.models import Item


def update_news_item_modify_at(apps, schema_editor):
    Item.objects.filter(modified_at__isnull=True).update(modified_at=F('created_at'))

class Migration(migrations.Migration):

    dependencies = [
        ('digest', '0004_item_modified_at'),
    ]

    operations = [
        migrations.RunPython(update_news_item_modify_at),
    ]
