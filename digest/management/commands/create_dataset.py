# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import os
from datetime import datetime, timedelta, date

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
            data = json.load(fio)
    else:
        data = {
            'links': []
        }

    items = Item.objects.filter(
        related_to_date__range=[start_date,
                                end_date])

    with open(out_filepath, 'w') as fio:
        for item in items:
            if not check_exist_link(data, item):
                data['links'].append(item.data4cls)
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
