# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

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

        for x in ItemClsCheck.objects.filter(item__id__in=ids):
            x.check_cls(force=True)
