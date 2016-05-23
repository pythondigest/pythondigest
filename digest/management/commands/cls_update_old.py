# -*- coding: utf-8 -*-


import datetime
import json

import requests
import simplejson
from django.conf import settings
from django.core.management import BaseCommand

from digest.models import ItemClsCheck, Item


def update_cls(items, part_size=100):
    cnt = items.count()
    cur_part = 0
    url = '{0}/{1}'.format(settings.CLS_URL_BASE, 'api/v1.0/classify/')
    items = list(items)
    while part_size * cur_part < cnt:
        print(cur_part)

        links_items = items[part_size * cur_part:part_size * (cur_part + 1)]
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


class Command(BaseCommand):
    help = 'Update old news'

    def handle(self, *args, **options):
        prev_date = datetime.datetime.now() - datetime.timedelta(days=10)
        items = Item.objects.filter(
            id__in=ItemClsCheck.objects.filter(
                last_check__lte=prev_date
            ).values_list('item', flat=True)
        )
        update_cls(items)
