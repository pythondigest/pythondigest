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
        parser.add_argument('percent', type=int)  # сколько частей

    def handle(self, *args, **options):
        """
        Основной метод - точка входа
        """

        items_cnt = Item.objects.exclude(link__icontains='allmychanges.com').count()

        train_size = math.ceil(items_cnt * (options['percent'] / 100))
        # test_size = items_cnt - train_size

        train_part_size = math.ceil(train_size / options['cnt_parts'])

        items = Item.objects.exclude(link__icontains='allmychanges.com').order_by('?')

        train_set = items[:train_size]
        test_set = items[train_size:]

        for part in range(options['cnt_parts']):
            name = 'data_{}_{}.json'.format(train_part_size, part)
            queryset = train_set[part * train_part_size: (part + 1) * train_part_size]
            create_dataset(queryset, name)

        with open(os.path.join(settings.DATASET_FOLDER, 'test_set_ids.txt'), 'w') as fio:
            fio.writelines(["%s\n" % x for x in test_set.values_list('id', flat=True)])
