# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from django.conf import settings
from django.core.management.base import BaseCommand
from django_q.tasks import async

from digest.models import Item


def get_article(item):
    path = os.path.join(settings.DATASET_ROOT, '{0}.html'.format(item.id))
    with open(path, 'w') as fio:
        try:
            text = item.text
        except Exception as e:
            text = ''
        
        fio.write(text)
        item.article_path = path
        item.save()
    return item.link


class Command(BaseCommand):
    help = 'Create dataset'

    def handle(self, *args, **options):
        """
        Основной метод - точка входа
        """
        if not os.path.isdir(settings.DATASET_ROOT):
            os.makedirs(settings.DATASET_ROOT)

        for item in Item.objects.all():
            if item.article_path is None or not item.article_path or not os.path.exists(item.article_path):
                async(get_article, item)
                # get_article(item)
