# -*- encoding: utf-8 -*-

from __future__ import unicode_literals

from django.core.management.base import BaseCommand

from digest.models import Issue
from digest.pub_digest import pub_to_all


class Command(BaseCommand):
    args = 'no arguments!'
    help = 'News import from external resources'

    def add_arguments(self, parser):
        parser.add_argument('issue', type=int)

    def handle(self, *args, **options):
        """
        Основной метод - точка входа
        """
        issue = Issue.objects.get(pk=options['issue'])
        site = 'http://pythondigest.ru'

        pub_to_all(
            issue.announcement,
            '{0}{1}'.format(site, issue.link),
            '{0}{1}'.format(site, issue.image.url if issue.image else ''))
