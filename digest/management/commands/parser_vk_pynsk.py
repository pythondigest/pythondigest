# -*- encoding: utf-8 -*-

from __future__ import unicode_literals
import datetime
import re
import textwrap
from time import mktime

from django.core.management.base import BaseCommand

import feedparser

from digest.management.commands import save_item

from digest.models import Item, Resource, Section

l = [
    'Тесты тесты тесты',
    'Внутренности Python',
    'Синтаксис Python',
    'Полезные инструменты',
    'Извлечение информации',
    'Таинство стандартной библиотеки',
    'Опыт разработчиков',
    'Python на службе народа',
    'Полезные библиотеки',
    'Hardcore Python',
    'Функциональный Python',
    'Пишем web-проекты',
    'Интересные концепции',
]


def main():
    url = 'http://feed.exileed.com/vk/feed/pynsk'

    _section_title = 'Колонка автора'
    _res_title = 'PyNSK - группа сообщества'

    resource = Resource.objects.filter(title=_res_title)
    assert resource.count() == 1, "Not found resoure: %s" % _res_title
    resource = resource[0]

    section = Section.objects.filter(title=_section_title)
    assert section.count() == 1, "Not found section: %s" % _section_title
    section = section[0]

    r = re.compile(r"(htt(p|ps)://[^ ]+)")

    today = datetime.date.today()
    week_before = today - datetime.timedelta(weeks=1)
    rssnews = feedparser.parse(url)
    for n in reversed(rssnews.entries):
        # if len(Item.objects.filter(link=n.link)[0:1]):
        #     continue

        # print("Parse: %s" % n.link)
        title = None
        content = None

        time_struct = getattr(n, 'published_parsed', None)
        if time_struct:
            _timestamp = mktime(time_struct)
            dt = datetime.datetime.fromtimestamp(_timestamp)
            if dt.date() < week_before:
                continue

        text = n.summary
        for x in l:
            if x in text and '<br><br>' in text.split(x)[1]:
                _ = text.split(x)[1].split('<br>')
                title = x + _[0]
                content = ' </br>\n'.join(filter(lambda x: x, _[1:]))

                content = r.sub(r'<a href="\1">\1</a>', content)
                break

        if title is not None and content is not None:
            content_link = "<a href='%s'>[Продолжение]</a>" % n.link
            content = textwrap.shorten(content, width=300, placeholder="...%s" % content_link)\
                .replace('<a...', '...')
            _ = {
                'link': n.link,
                'description': content,
                'title': title,
                'resource': resource,
                'language': 'ru',
                'section': section,
                'status': 'active',
            }
            save_item(_)


class Command(BaseCommand):
    args = 'no arguments!'
    help = u'News import from external resources'

    def handle(self, *args, **options):
        main()
