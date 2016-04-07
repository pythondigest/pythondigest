# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.management.base import BaseCommand

from digest.models import ItemClsCheck


class Command(BaseCommand):
    help = u'lala'

    def handle(self, *args, **options):
        for x in ItemClsCheck.objects.all():
            x.check_cls(force=True)
