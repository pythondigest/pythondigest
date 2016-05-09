# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.management.base import BaseCommand

from digest.models import ItemClsCheck


class Command(BaseCommand):
    help = 'lala'

    def handle(self, *args, **options):
        ItemClsCheck.objects.all().update(status=False)
