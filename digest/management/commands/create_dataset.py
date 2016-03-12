# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import os
from datetime import datetime, timedelta, date

import grequests
from django.conf import settings
from django.core.management.base import BaseCommand

from digest.models import Item, get_start_end_of_week


def check_exist_link(data, item):
    for info in data.get('links'):
        if info['link'] == item.link:
            return True
    else:
        return False


def create_dataset(start_date, end_date, name):
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

    items = {x.link: x for x in Item.objects.filter(
        related_to_date__range=[
            start_date,
            end_date
        ])[:5] if not check_exist_link(data, x)}

    rs = (grequests.get(u) for u in items.keys())
    resps = grequests.map(rs)

    for res in resps:
        data['links'].append(items[res.url].get_data4cls(status=True, text=items[res.url].get_text(res.text)))

    if not os.path.exists(os.path.dirname(out_filepath)):
        os.makedirs(os.path.dirname(out_filepath))

    with open(out_filepath, 'w') as fio:
        json.dump(data, fio)


class Command(BaseCommand):
    help = u'Create dataset'

    def add_arguments(self, parser):
        parser.add_argument('year', type=int)
        parser.add_argument('week', type=int)

    def handle(self, *args, **options):
        """
        Основной метод - точка входа
        """
        assert 0 <= options['week'] <= 52, "Not valid week cnt"

        data = datetime.strptime('%04d-%02d-1' % (options['year'], options['week']), '%Y-%W-%w')
        if date(options['year'], 1, 4).isoweekday() > 4:
            data -= timedelta(days=7)

        start, end = get_start_end_of_week(data)
        name = 'data_{}_{}.json'.format(options['year'], options['week'])
        create_dataset(start, end, name)
