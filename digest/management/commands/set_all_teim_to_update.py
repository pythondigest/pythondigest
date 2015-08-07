# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.management.base import BaseCommand

from digest.management.commands import save_pickle_file

from digest.models import Item


class Command(BaseCommand):
    args = 'no arguments!'
    help = u'News import from external resources'

    def handle(self, *args, **options):
        """
        Основной метод - точка входа
        """
        items = Item.objects.all()
        save_pickle_file('./pk_list.pickle',
                         list(items.values_list('pk', flat=True)))
        items.update(to_update=True)
