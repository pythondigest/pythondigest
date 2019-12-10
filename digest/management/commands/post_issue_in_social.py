# -*- encoding: utf-8 -*-

from __future__ import unicode_literals

from django.core.management.base import BaseCommand

from digest.models import Issue
from digest.pub_digest import pub_to_all


def prepare_issue_news(issue: Issue):
    news = issue.item_set
    result = {}

    for x in news.filter(status='active').iterator():
        if x.section not in result:
            result[x.section] = []
        result[x.section].append({
            "link": x.link,
            "title": x.title,
            "description": x.description,
            "tags": [],
        })
    result = sorted(result.items(),
                    key=lambda x: x[0].priority,
                    reverse=True)
    result = [{'category': x.title, 'news': y} for x, y in result]
    return result


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
            issue.title,
            issue.announcement,
            '{0}{1}'.format(site, issue.link),
            '{0}{1}'.format(site, issue.image.url if issue.image else ''),
            prepare_issue_news(issue)
        )
