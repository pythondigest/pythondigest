# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from django.db.models import Q

from digest.management.commands.create_dataset import create_dataset
from digest.models import Item


class Command(BaseCommand):
    help = 'Create dataset'

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

        # TODO make raw sql
        active_news = Item.objects.filter(status='active').exclude(query)
        links = active_news.all().values_list('link', flat=True).distinct()
        non_active_news = Item.objects.exclude(link__in=links).exclude(query)

        items_ids = list(active_news.values_list('id', flat=True))
        items_ids.extend(non_active_news.values_list('id', flat=True))
        items_ids = list(set(items_ids))

        items = Item.objects.filter(id__in=items_ids)

        create_dataset(items, 'items.json')
