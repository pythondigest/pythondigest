# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from syncrss.updater import update_rss


class Command(BaseCommand):
    
    args = 'no arguments!'
    help = u''

    def handle(self, *args, **options):
        '''
        Основной метод - точка входа
        '''
        update_rss()
