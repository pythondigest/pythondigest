# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.management.base import BaseCommand
import lxml.html as html
from lxml import etree

from digest.management.commands import apply_parsing_rules, apply_video_rules, save_item
from digest.models import ParsingRules, Section, Tag, ITEM_STATUS_CHOICES, Resource


def import_python_weekly(issue_url, **kwargs):
    resource = Resource.objects.get(title='PythonWeekly')

    page = html.parse(issue_url)

    # a = requests.get(url).content
    blocks = page.getroot().find_class('bodyTable')[0].xpath('//span[@style="font-size:14px"]')

    for x in blocks:
        link = x.cssselect('a')[0]
        url = link.attrib['href']
        title = link.text
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


def main():
    url = 'http://us2.campaign-archive.com/?u=e2e180baf855ac797ef407fc7&id=14f4381681'

    data = {
        'query_rules': ParsingRules.objects.filter(is_activated=True).all(),
        'query_sections': Section.objects.all(),
        'query_tags': Tag.objects.all(),
        'query_statuses': [x[0] for x in ITEM_STATUS_CHOICES],
    }
    import_python_weekly(url, **data)


class Command(BaseCommand):
    args = 'no arguments!'
    help = u''

    def handle(self, *args, **options):
        main()
