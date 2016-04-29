# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.management.base import BaseCommand
from django.db.models import Q

from digest.management.commands.create_dataset import create_dataset
from digest.models import Item


class Command(BaseCommand):
    help = u'Create dataset'

    def handle(self, *args, **options):
        """
        Основной метод - точка входа
        """

        query = Q()

        urls = [
            'allmychanges.com',
            'stackoverflow.com',
        ]
        for entry in urls:
            query = query | Q(link__contains=entry)

        create_dataset(Item.objects.exclude(query).order_by('?'), 'items.json')
