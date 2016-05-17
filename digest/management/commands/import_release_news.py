# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
from time import mktime

import feedparser
from django.core.management.base import BaseCommand

from digest.management.commands import save_item
from digest.models import Item, get_start_end_of_week
from digest.models import Package, Section, Resource, Issue


def _generate_release_item(package_version: str, link: str,
                           resource: Resource, section: Section,
                           package_data: dict):
    name = '{0} - {1}'.format(package_data.get('name'), package_version)
    description = '{2}.' \
                  ' Изменения описаны по ссылке <a href="{3}">{3}</a>. ' \
                  'Скачать можно по ссылке: <a href="{4}">{4}</a>'.format(
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


def off_other_release_news(news, package_data):
    news.filter(title__startswith=package_data.get('name'),
                description__contains=package_data.get('url')).update(
        status='moderated')


def check_previous_news_of_package(news, package_data):
    items = news.filter(title__startswith=package_data.get('name'),
                        description__contains=package_data.get('url'))
    assert items.count() <= 1, 'Many items for library'
    return items.count() != 0


def parse_rss():
    url = 'https://allmychanges.com/rss/03afbe621916b2f2145f111075db0759/'

    today = datetime.date.today()
    week_before = today - datetime.timedelta(weeks=1)
    try:
        packages = {
            x.get('name').strip(): x
            for x in list(Package.objects.all()
                          .values('name', 'description', 'link'))
            }
        _start_week, _end_week = get_start_end_of_week(today)
        _ = Issue.objects.filter(date_from=_start_week, date_to=_end_week)

        assert _.count() <= 1, 'Many ISSUE on week'
        _ = None if _.count() == 0 else _[0]
        news = Item.objects.filter(issue=_,
                                   status='active') if _ is not None else []

        section = Section.objects.get(title='Релизы')
        resource = Resource.objects.get(link='http://allmychanges.com/')
    except Exception as e:
        print(e)
        return

    saved_packages = []
    for n in feedparser.parse(url).entries:
        package_name, package_version = n.title.split()
        package_name = package_name.replace('python/', '')

        ct = len(Item.objects.filter(link=n.link, status='active')[0:1])
        if ct or not ('python' in n.title):
            saved_packages.append(package_name)
            continue

        time_struct = getattr(n, 'published_parsed', None)
        if time_struct:
            _timestamp = mktime(time_struct)
            dt = datetime.datetime.fromtimestamp(_timestamp)
            if dt.date() < week_before:
                continue

        try:
            if not (package_name in
                        packages.keys()) or package_name in saved_packages:
                continue

            if news and check_previous_news_of_package(news, packages.get(
                package_name)):
                off_other_release_news(news, packages.get(package_name))

            item_data = _generate_release_item(package_version,
                                               n.link, resource, section,
                                               packages.get(package_name))
            saved_packages.append(package_name)
            save_item(item_data)
        except Exception as e:
            print(e)
            continue


class Command(BaseCommand):
    args = 'no arguments!'
    help = 'News import from external resources'

    def handle(self, *args, **options):
        parse_rss()
