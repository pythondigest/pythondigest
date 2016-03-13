# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime, timedelta, date

from django.core.management.base import BaseCommand

from digest.management.commands.create_dataset_ids import create_dataset
from digest.models import Item, get_start_end_of_week


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

        items = Item.objects.filter(
            related_to_date__range=[
                start,
                end
            ])

        create_dataset(items, name)
