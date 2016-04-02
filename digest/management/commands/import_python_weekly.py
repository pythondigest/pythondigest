# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from urllib.request import urlopen

import lxml.html as html
from django.core.management.base import BaseCommand
from lxml import etree

from digest.management.commands import apply_parsing_rules, apply_video_rules, save_item
from digest.models import ParsingRules, Section, ITEM_STATUS_CHOICES, Resource


def _get_content(url):
    return urlopen(url, timeout=10).read()


def _get_blocks(url):
    page = html.parse(_get_content(url))
    return page.getroot().find_class('bodyTable')[0].xpath('//span[@style="font-size:14px"]')


def import_python_weekly(issue_url, **kwargs):
    resource = Resource.objects.get(title='PythonWeekly')

    for x in _get_blocks(issue_url):
        link = x.cssselect('a')[0]
        url = link.attrib['href']
        title = link.text
        _text = x.getnext()
        if _text is None:
            continue
        text = etree.tostring(x.getnext()).decode('utf-8').replace('<br/>', '').strip()

        item_data = {
            'title': title,
            'link': url,
            'raw_content': text,
            'http_code': 200,
            'content': text,
            'description': text,
            'resource': resource,
            'language': 'en',
        }
        item_data.update(
            apply_parsing_rules(item_data, **kwargs)
            if kwargs.get('query_rules') else {})
        item_data = apply_video_rules(item_data.copy())
        save_item(item_data)


def main(url):
    data = {
        'query_rules': ParsingRules.objects.filter(is_activated=True).all(),
        'query_sections': Section.objects.all(),
        'query_statuses': [x[0] for x in ITEM_STATUS_CHOICES],
    }
    import_python_weekly(url, **data)


class Command(BaseCommand):
    args = 'no arguments!'
    help = u''

    def add_arguments(self, parser):
        parser.add_argument('url', type=str)

    def handle(self, *args, **options):
        if 'url' in options:
            main(options['url'])
        else:
            print('Not found folder path')
