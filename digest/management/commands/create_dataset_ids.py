# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import math
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from digest.models import Item


def check_exist_link(data, item):
    for info in data.get('links'):
        if info['link'] == item.link:
            return True
    else:
        return False


def create_dataset(queryset_items, name):
    if not queryset_items:
        return
    out_filepath = os.path.join(settings.DATASET_FOLDER, name)
    data = {'links': [
        x.get_data4cls(status=True) for x in queryset_items
        ]}

    if not os.path.exists(os.path.dirname(out_filepath)):
        os.makedirs(os.path.dirname(out_filepath))

    with open(out_filepath, 'w') as fio:
        json.dump(data, fio)


class Command(BaseCommand):
    help = u'Create dataset'

    def add_arguments(self, parser):
        parser.add_argument('cnt_parts', type=int)  # сколько частей

    def handle(self, *args, **options):
        """
        Основной метод - точка входа
        """

        count = math.ceil(Item.objects.all().count() / options['cnt_parts'])
        for part in range(options['cnt_parts'] + 1):
            name = 'data_{}_{}.json'.format(count, part)
            items = Item.objects.all().order_by('id')[part * count: (part + 1) * count]
            create_dataset(items, name)
            break
