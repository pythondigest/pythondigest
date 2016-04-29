# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import glob
import json
import math
import os
import random

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.models import Q

from digest.models import Item


def check_exist_link(data, item):
    for info in data.get('links'):
        if info['link'] == item.link:
            return True
    else:
        return False


def save_dataset(data_items, name):
    if not data_items:
        return
    out_filepath = os.path.join(settings.DATASET_FOLDER, name)
    data = {'links': data_items}

    if not os.path.exists(os.path.dirname(out_filepath)):
        os.makedirs(os.path.dirname(out_filepath))

    with open(out_filepath, 'w') as fio:
        json.dump(data, fio)


class Command(BaseCommand):
    help = u'Create dataset'

    def add_arguments(self, parser):
        parser.add_argument('cnt_parts', type=int)  # сколько частей
        parser.add_argument('percent', type=int)  # сколько частей
        parser.add_argument('dataset_folder', type=str)  # ссылка на дополнительный датасет для объединения

    def handle(self, *args, **options):
        """
        Основной метод - точка входа
        """

        """
        У меня есть датасет, который находится вне дайджеста (просто файлом)
        И есть данные которые в самом дайджесте

        Надо иметь возможность в автоматическом режиме объединять эти два датасета
        И делать датасет для обучения и для тренировки

        После тренировки по датасету надо сделать репорт.
        Проблема в том, что у датасета, которого нет в БД, нет id-шнкиков.
        """

        assert os.path.exists(options['dataset_folder'])
        additional_data = []
        for x in glob.glob('%s/*.json' % options['dataset_folder']):
            with open(x, 'r') as fio:
                additional_data.extend(json.load(fio)['links'])

        query = Q()

        urls = [
            'allmychanges.com',
            'stackoverflow.com',
        ]
        for entry in urls:
            query = query | Q(link__contains=entry)

        items = Item.objects.exclude(query).exclude(section=None).order_by('?')
        items_data = [x.get_data4cls(status=True) for x in items]
        items_data.extend(additional_data)
        random.shuffle(items_data)
        items_cnt = len(items_data)

        train_size = math.ceil(items_cnt * (options['percent'] / 100))
        test_size = items_cnt - train_size
        train_part_size = math.ceil(train_size / options['cnt_parts'])
        test_part_size = math.ceil(test_size / options['cnt_parts'])

        train_set = items_data[:train_size]
        test_set = items_data[train_size:]

        for part in range(options['cnt_parts']):
            train_name = 'train_{0}_{1}.json'.format(train_part_size, part)
            test_name = 'test_{0}_{1}.json'.format(test_part_size, part)
            save_dataset(train_set[part * train_part_size: (part + 1) * train_part_size], train_name)
            save_dataset(test_set[part * test_part_size: (part + 1) * test_part_size], test_name)
