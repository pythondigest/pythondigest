# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import os

import grequests
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

    if os.path.exists(out_filepath):
        with open(out_filepath, 'r') as fio:
            try:
                data = json.load(fio)
            except ValueError as e:
                print(e)
                data = {'links': []}
    else:
        data = {'links': []}

    items = {x.link: x for x in queryset_items if not check_exist_link(data, x)}

    rs = (grequests.get(u) for u in items.keys())
    resps = grequests.map(rs)

    for res in resps:
        try:
            data['links'].append(items[res.url].get_data4cls(status=True, text=items[res.url].get_text(res.text)))
        except KeyError as e:
            print("Not found key '{}'".format(res.url))
        except AttributeError as e:
            continue

    if not os.path.exists(os.path.dirname(out_filepath)):
        os.makedirs(os.path.dirname(out_filepath))

    with open(out_filepath, 'w') as fio:
        json.dump(data, fio)


class Command(BaseCommand):
    help = u'Create dataset'

    def add_arguments(self, parser):
        parser.add_argument('count', type=int)  # сколько элементов в части
        parser.add_argument('part', type=int)  # какая часть

    def handle(self, *args, **options):
        """
        Основной метод - точка входа
        """
        count = options['count']
        part = options['part']
        name = 'data_{}_{}.json'.format(options['count'], options['part'])

        items = Item.objects.all().order_by('id')[part * count: (part + 1) * count]

        create_dataset(items, name)
