# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import re
from time import mktime

import feedparser
from django.core.management.base import BaseCommand

from digest.management.commands import _get_http_data_of_url, \
    apply_parsing_rules, get_tweets_by_url, save_item, apply_video_rules, is_weekly_digest, parse_weekly_digest
from digest.models import ITEM_STATUS_CHOICES, \
    AutoImportResource, Item, ParsingRules, Section


def get_tweets():
    dsp = []
    for src in AutoImportResource.objects.filter(type_res='twitter',
                                                 in_edit=False):

        resource = src.resource
        excl = [s for s in (src.excl or '').split(',') if s]

        tweets_data = get_tweets_by_url(src.link)

        for text, link, http_code in tweets_data:
            excl_link = bool([i for i in excl if i in link])
            if not excl_link and src.incl in text:
                tw_txt = text.replace(src.incl, '')
                dsp.append([tw_txt, link, resource, http_code])
    return dsp


def import_tweets(**kwargs):
    for i in get_tweets():
        # это помогает не парсить лишний раз ссылку, которая есть
        if Item.objects.filter(link=i[1]).exists():
            continue

        # title = u'[!] %s' % i[0] if fresh_google_check(i[1]) else i[0]
        title = i[0]
        item_data = {
            'title': title,
            'link': i[1],
            'http_code': i[3],
            'resource': i[2]
        }
        if is_weekly_digest(item_data):
            parse_weekly_digest(item_data)
        else:
            data = apply_parsing_rules(item_data, **kwargs) if kwargs.get(
                'query_rules') else {}
            item_data.update(data)
        save_item(item_data)


def import_rss(**kwargs):
    for src in AutoImportResource.objects.filter(type_res='rss',
                                                 in_edit=False):

        rssnews = feedparser.parse(src.link)
        today = datetime.date.today()
        week_before = today - datetime.timedelta(weeks=1)
        for n in rssnews.entries:
            ct = len(Item.objects.filter(link=n.link)[0:1])
            if ct:
                continue

            time_struct = getattr(n, 'published_parsed', None)
            if time_struct:
                _timestamp = mktime(time_struct)
                dt = datetime.datetime.fromtimestamp(_timestamp)
                if dt.date() < week_before:
                    continue

            title = n.title
            # title = u'[!] %s' % n.title if fresh_google_check(
            #    n.title) else n.title

            http_code, content, raw_content = _get_http_data_of_url(n.link)

            try:
                summary = re.sub('<.*?>', '', n.summary)
            except (AttributeError, KeyError):
                summary = ''

            item_data = {
                'title': title,
                'link': n.link,
                'raw_content': raw_content,
                'http_code': http_code,
                'content': content,
                'description': summary,
                'resource': src.resource,
                'language': src.language,
            }

            if is_weekly_digest(item_data):
                parse_weekly_digest(item_data)
            else:
                item_data.update(
                    apply_parsing_rules(item_data, **kwargs)
                    if kwargs.get('query_rules') else {})
                item_data = apply_video_rules(item_data.copy())
            save_item(item_data)


def parsing(func):
    """

    :param func:
    :return:
    """
    data = {
        'query_rules': ParsingRules.objects.filter(is_activated=True).all(),
        'query_sections': Section.objects.all(),
        'query_statuses': [x[0] for x in ITEM_STATUS_CHOICES]
    }
    func(**data)


class Command(BaseCommand):
    args = 'no arguments!'
    help = u'News import from external resources'

    def handle(self, *args, **options):
        """
        Основной метод - точка входа
        """
        parsing(import_tweets)
        parsing(import_rss)
