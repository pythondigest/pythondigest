# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.management.base import BaseCommand

from digest.management.commands.import_news import get_tweets_by_url
from digest.models import Package, Section, Resource
from digest.management.commands import save_item



def parse():
    base_url = 'https://twitter.com/NewReleaseNotes/'
    packages = list(Package.objects.all().values('name', 'description', 'url'))

    if packages:
        try:
            section = Section.objects.get(title=u'Релизы')
            resource = Resource.objects.get(link='http://allmychanges.com/')
        except Exception:
            return

        tweets_data = get_tweets_by_url(base_url)

        for text, link, http_code in tweets_data:
            for x in packages:
                if 'python' in text and "python/%s" % x.get(
                        'name').lower() in text:
                    name = u"{} - {}".format(
                        x.get('name'),
                        text.split(' of')[0]
                    )
                    description = u"Вышла новая версия пакета {0} - {1}." \
                                  u" {2}." \
                                  u" Изменения описаны по ссылке <a href='{3}'>{3}</a>. " \
                                  u"Скачать можно по ссылке: <a href='{4}'>{4}</a>".format(
                        x.get('name'),
                        text.split(' of')[0],
                        x.get('description'),
                        link,
                        x.get('url')
                    )

                    save_item({
                        'title': name,
                        'link': link,
                        'resource': resource,
                        'status': 'active',
                        'section': section,
                        'language': 'en',
                        'description': description,
                    })

class Command(BaseCommand):
    args = 'no arguments!'
    help = u'News import from external resources'

    def handle(self, *args, **options):
        '''
        Основной метод - точка входа
        '''
        parse()
