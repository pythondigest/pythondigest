# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
from time import mktime

from django.core.management.base import BaseCommand
import feedparser
from funcy import join

from jobs.models import JobFeed, JobItem, RejectedList, AcceptedList


def parse_feed(feed_url):
    print(feed_url)
    # rssnews = feedparser.parse(feed_url)
    # today = datetime.date.today()
    # week_before = today - datetime.timedelta(weeks=1)
    # for n in rssnews.entries:
    #     ct = len(Item.objects.filter(link=n.link)[0:1])
    #     if ct:
    #         continue
    #
    #     time_struct = getattr(n, 'published_parsed', None)
    #     if time_struct:
    #         _timestamp = mktime(time_struct)
    #         dt = datetime.datetime.fromtimestamp(_timestamp)
    #         if dt.date() < week_before:
    #             continue
    #
    #     title = n.title
    #     # title = u'[!] %s' % n.title if fresh_google_check(
    #     #    n.title) else n.title
    #
    #     http_code, content, raw_content = _get_http_data_of_url(n.link)
    #
    #     item_data = {
    #         'title': title,
    #         'link': n.link,
    #         'raw_content': raw_content,
    #         'http_code': http_code,
    #         'content': content,
    #         'description': re.sub('<.*?>', '', n.summary),
    #         'resource': src.resource,
    #         'language': src.language,
    #     }
    #     item_data.update(
    #         apply_parsing_rules(item_data, **kwargs)
    #         if kwargs.get('query_rules') else {})
    #     item_data = apply_video_rules(item_data.copy())
    #     save_item(item_data)

def filter_excl(item_data):
    excl = [s for s in (src.excl or '').split(',') if s]

    tweets_data = get_tweets_by_url(src.link)

    for text, link, http_code in tweets_data:
        excl_link = bool([i for i in excl if i in link])
        if not excl_link and src.incl in text:
            tw_txt = text.replace(src.incl, '')
            dsp.append([tw_txt, link, resource, http_code])


def get_link_title_desc(item):
    result = None, None, None
    if item:
        assert item.title, "Not found title in item"
        assert item.link, "Not found link in item"

        link = item.link.replace(u'https://www.google.com/url?rct=j&sa=t&url=',
                                 '')
        ge_ind = link.find('&ct=ga')
        if ge_ind > -1:
            link = link[0:ge_ind]
        title = item.title.replace('<b>', '').replace('</b>', '')
        result = link, title, item.summary
    return result

def get_rss_items(feed_url):
    items = feedparser.parse(feed_url)
    result = []
    for n in items.entries:
        if JobItem.objects.filter(link=n.link).exists():
            continue
        result.append(n)
    return result


def is_new_job(item):
    result = True
    today = datetime.date.today()
    week_before = today - datetime.timedelta(weeks=1)
    time_struct = getattr(item, 'published_parsed', None)
    if time_struct:
        _timestamp = mktime(time_struct)
        dt = datetime.datetime.fromtimestamp(_timestamp)
        if dt.date() < week_before:
            result = False
    return result


def import_jobs():
    _job_feeds_obj = JobFeed.objects.filter(in_edit=False)
    job_feeds = list(_job_feeds_obj.values_list('link', flat=True))
    items = map(get_link_title_desc,
        join(
        filter(is_new_job,
        map(get_rss_items, job_feeds))))

    excl = list(RejectedList.objects.values_list('title', flat=True))
    # todo
    # примнеять список разрешения
    # incl = list(AcceptedList.objects.values_list('title', flat=True))

    for link, title, description in items:
        excl_link = bool([i for i in excl if i in link])
        if not excl_link:
            print(description)

    # print(list(a))


class Command(BaseCommand):
    args = 'no arguments!'
    help = u'News import from external resources'

    def handle(self, *args, **options):
        """
        Основной метод - точка входа
        """
        import_jobs()
