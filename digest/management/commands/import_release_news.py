# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
from time import mktime

import feedparser
from django.core.management.base import BaseCommand

from digest.models import Item
from digest.management.commands import save_item
from digest.models import Package, Section, Resource


def _generate_release_item(package_name: str,
                           package_version: str,
                           link: str,
                           resource: Resource,
                           section: Section,
                           package_data: dict):
    name = u"{} - {}".format(
        package_data.get('name'),
        package_version
    )
    description = u"{2}." \
                  u" Изменения описаны по ссылке <a href='{3}'>{3}</a>. " \
                  u"Скачать можно по ссылке: <a href='{4}'>{4}</a>".format(
        package_data.get('name'),
        package_version,
        package_data.get('description'),
        link,
        package_data.get('url')
    )

    return {
        'title': name,
        'link': link,
        'resource': resource,
        'status': 'active',
        'section': section,
        'language': 'en',
        'description': description,
    }

def parse_rss():
    # todo
    # hardcode
    # это личная лента модератора
    # по возможности заменить на ленту спец. созданную для pydigest
    url = 'https://allmychanges.com/rss/05a5ec600331b03741bd08244afa11cb/'

    try:
        packages = {x.get('name'): x for x in
                    list(Package.objects.all()
                         .values('name', 'description', 'url'))}
        section = Section.objects.get(title=u'Релизы')
        resource = Resource.objects.get(link='http://allmychanges.com/')
    except Exception:
        return

    today = datetime.date.today()
    week_before = today - datetime.timedelta(weeks=1)
    saved_packages = []
    for n in feedparser.parse(url).entries:
        ct = len(Item.objects.filter(link=n.link)[0:1])
        if ct or not ('python' in n.title):
            continue

        time_struct = getattr(n, 'published_parsed', None)
        if time_struct:
            _timestamp = mktime(time_struct)
            dt = datetime.datetime.fromtimestamp(_timestamp)
            if dt.date() < week_before:
                continue

        try:
            package_name, package_version = n.title.split()

            package_name = package_name.replace('python/', '')
            if not (package_name in packages.keys()) or package_name in saved_packages:
                continue

            item_data = _generate_release_item(
                package_name,
                package_version,
                n.link,
                resource,
                section,
                packages.get(package_name)
            )
            saved_packages.append(package_name)
            save_item(item_data)
        except Exception as e:
            continue


class Command(BaseCommand):
    args = 'no arguments!'
    help = u'News import from external resources'

    def handle(self, *args, **options):
        parse_rss()
