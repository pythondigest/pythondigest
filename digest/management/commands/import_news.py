# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import re
import socket
from time import mktime
from typing import Dict, List
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

import feedparser
from django.core.management.base import BaseCommand
from requests import TooManyRedirects

from digest.management.commands import (_get_http_data_of_url,
                                        apply_parsing_rules, apply_video_rules,
                                        get_tweets_by_url,
                                        is_django_weekly_digest,
                                        is_weekly_digest,
                                        parse_django_weekly_digest,
                                        parse_weekly_digest, save_item)
from digest.models import (ITEM_STATUS_CHOICES, AutoImportResource, Item,
                           ParsingRules, Section)


def _parse_tweets_data(data: list, src: AutoImportResource) -> list:
    result = []
    excl = [s.strip() for s in (src.excl or '').split(',') if s]
    for text, link, http_code in data:

        try:
            excl_link = bool([i for i in excl if i in link])
        except TypeError as e:
            print("WARNING: (import_news): {}".format(e))
            excl_link = False
        if not excl_link and src.incl in text:
            tw_txt = text.replace(src.incl, '')
            result.append([tw_txt, link, src.resource, http_code])
    return result


def get_tweets():
    dsp = []
    for src in AutoImportResource.objects.filter(type_res='twitter',
                                                 in_edit=False):
        print("Process twitter", src)
        try:
            dsp.extend(_parse_tweets_data(get_tweets_by_url(src.link), src))
        except Exception as e:
            print(e)
    return dsp


def import_tweets(**kwargs):
    for i in get_tweets():
        try:
            # это помогает не парсить лишний раз ссылку, которая есть
            if Item.objects.filter(link=i[1]).exists():
                continue

            # title = '[!] %s' % i[0] if fresh_google_check(i[1]) else i[0]
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
        except (URLError, TooManyRedirects, socket.timeout) as e:
            print(i, str(e))


def get_items_from_rss(rss_link: str) -> List[Dict]:
    """
    Get rss content from rss source.

    Function create request to rss source, parse RSS and create list of dict with rss data
    (link, title, description and news data)
    :param rss_link: string, rss link
    :return: list of dicts, each dict includes link, title, description and news data of rss item
    """
    rss_items = []
    try:
        response = urlopen(rss_link, timeout=10)
        res_news = feedparser.parse(response.read())
        response.close()

        for n in res_news.entries:

            news_time = getattr(n, 'published_parsed', None)
            if news_time is not None:
                _timestamp = mktime(news_time)
                news_date = datetime.datetime.fromtimestamp(_timestamp).date()
            else:
                news_date = datetime.date.today()

            # create data dict
            try:
                summary = re.sub('<.*?>', '', n.summary)
            except (AttributeError, KeyError):
                summary = ''

            rss_items.append({
                'title': n.title,
                'link': n.link,
                'description': summary,
                'related_to_date': news_date,
            })
    except Exception as e:
        print("Exception -> ", str(e))
        rss_items = []

    return rss_items


def _is_old_rss_news(rss_item: Dict, minimum_date=None) -> bool:
    if minimum_date is None:
        minimum_date = datetime.date.today() - datetime.timedelta(weeks=1)
    return rss_item['related_to_date'] > minimum_date


def is_not_exists_rss_item(rss_item: Dict, minimum_date=None) -> bool:
    if minimum_date is None:
        minimum_date = datetime.date.today() - datetime.timedelta(weeks=1)

    return not Item.objects.filter(
        link=rss_item['link'],
        related_to_date__gte=minimum_date
    ).exists()


def get_data_for_rss_item(rss_item: Dict) -> Dict:
    http_code, content, raw_content = _get_http_data_of_url(rss_item['link'])
    rss_item.update(
        {
            'raw_content': raw_content,
            'http_code': http_code,
            'content': content,
        }
    )
    return rss_item


def import_rss(**kwargs):
    for src in AutoImportResource.objects.filter(type_res='rss',
                                                 in_edit=False):
        print("Process RSS", src)
        try:
            rss_items = map(get_data_for_rss_item,
                            filter(is_not_exists_rss_item,
                                   filter(_is_old_rss_news,
                                          get_items_from_rss(src.link))))

            # parse weekly digests
            digests_items = list(rss_items)
            list(map(parse_weekly_digest,
                     filter(is_weekly_digest, digests_items)))

            list(map(parse_django_weekly_digest,
                     filter(is_django_weekly_digest, digests_items)))

            resource = src.resource
            language = src.language
            for i, rss_item in enumerate(digests_items):
                rss_item.update({
                    'resource': resource,
                    'language': language,
                })
                rss_item.update(
                    apply_parsing_rules(rss_item, **kwargs) if kwargs.get(
                        'query_rules') else {})
                rss_item.update(apply_video_rules(rss_item.copy()))
                save_item(rss_item)
        except (URLError, TooManyRedirects, socket.timeout) as e:
            print(src, str(e))


def parsing(func):
    data = {
        'query_rules': ParsingRules.objects.filter(is_activated=True).all(),
        'query_sections': Section.objects.all(),
        'query_statuses': [x[0] for x in ITEM_STATUS_CHOICES],
    }
    func(**data)


class Command(BaseCommand):
    args = 'no arguments!'
    help = 'News import from external resources'

    def handle(self, *args, **options):
        """
        Основной метод - точка входа
        """
        parsing(import_tweets)
        parsing(import_rss)
