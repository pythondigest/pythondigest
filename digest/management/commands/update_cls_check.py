# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import os

import requests
import simplejson
from django.conf import settings
from django.core.management.base import BaseCommand

from digest.models import ItemClsCheck


class Command(BaseCommand):
    help = u'Create dataset'

    def add_arguments(self, parser):
        parser.add_argument('input_path', type=str)

    def handle(self, *args, **options):
        """
        Основной метод - точка входа
        """
        ids = []

        if os.path.isfile(options['input_path']):
            with open(options['input_path'], 'r') as fio:
                ids = [int(x.strip()) for x in fio.readlines()]

        part_size = 100
        cur_part = 0
        url = "{0}/{1}".format(settings.CLS_URL_BASE, 'api/v1.0/classify/')

        items = ItemClsCheck.objects.filter(item__id__in=ids)
        cnt = items.count()
        while part_size * cur_part < cnt:
            print(cur_part)

            links_items = items._clone()
            links_items = links_items[part_size * cur_part:part_size * (cur_part + 1)]
            data = {
                'links':
                    [x.item.data4cls for x in links_items]
            }

            try:
                resp = requests.post(url, data=json.dumps(data))
                resp_data = {}
                for x in resp.json()['links']:
                    for key, value in x.items():
                        resp_data[key] = value
            except (requests.exceptions.RequestException,
                    requests.exceptions.Timeout,
                    requests.exceptions.TooManyRedirects,
                    simplejson.scanner.JSONDecodeError) as e:
                resp_data = None

            for x in links_items:
                if resp_data is None:
                    status = False
                else:
                    status = resp_data.get(x.item.link, False)
                x.status = status
                x.save()

            cur_part += 1