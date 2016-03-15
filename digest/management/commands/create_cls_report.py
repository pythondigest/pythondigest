# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import csv
import os

from django.core.management.base import BaseCommand

from digest.models import ItemClsCheck


class Command(BaseCommand):
    help = u'Create dataset'

    def add_arguments(self, parser):
        parser.add_argument('out_path', type=str)

    def handle(self, *args, **options):
        """
        Основной метод - точка входа
        """
        data = []
        for x in ItemClsCheck.objects.all():
            data.append(
                {
                    'link': x.item.link,
                    'moderator': x.item.status == 'active',
                    'classificator': x.status
                }
            )

        out_path = os.path.abspath(os.path.normpath(options['out_path']))
        if not os.path.isdir(os.path.dirname(out_path)):
            os.makedirs(os.path.dirname(out_path))

        with open(out_path, 'w') as fio:

            fieldnames = data[0].keys()
            writer = csv.DictWriter(fio, fieldnames=fieldnames)
            headers = dict((n, n) for n in fieldnames)
            writer.writerow(headers)
            for i in data:
                writer.writerow(i)
