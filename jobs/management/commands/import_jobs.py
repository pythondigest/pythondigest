# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
from functools import partial
from time import mktime

from django.core.management.base import BaseCommand
import feedparser
from funcy import join

from jobs.models import JobFeed, JobItem, RejectedList, AcceptedList


def get_link_title_desc(item: feedparser.FeedParserDict) -> tuple:
    """
    Для RSS Item возвращает ссылку, заголовок и описание
    :param item:
    :return:
    """
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


def get_rss_items(feed_url: str) -> list:
    """
    Возвращает список новостей из RSS
        проверяет что такой новости еще не сохранено
    :param feed_url:
    :return:
    """
    items = feedparser.parse(feed_url)
    result = []
    for n in items.entries:
        if JobItem.objects.filter(link=n.link).exists():
            continue
        result.append(n)
    return result


def is_new_job(item: feedparser.FeedParserDict) -> bool:
    """
    Возвращает True, если новость не старше недели
    :param item:
    :return:
    """
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


def is_not_excl(words: list, item: tuple) -> bool:
    """
    Возвращает True если ни один из элементов item
    не содержит слов из списка на исключения
    :param words:
    :param item:
    :return:
    """
    return not bool([i for x in item for i in words if i in x])


def is_incl(words: list, item: tuple) -> bool:
    """
    Возвращает True если хотя бы один элемент item
    :param words:
    :param item:
    :return:
    """
    for elem in item:
        for word in words:
            if word in elem:
                return True
    return False


def save_job(item: tuple) -> None:
    """
    Функция для сохранения
    :param item:
    :return:
    """
    link, title, description = item
    if not JobItem.objects.filter(link=link).exists():
        JobItem(
            link=link,
            title=title,
            description=description,
        ).save()

def import_jobs():
    _job_feeds_obj = JobFeed.objects.filter(in_edit=False)
    job_feeds = list(_job_feeds_obj.values_list('link', flat=True))
    excl = list(RejectedList.objects.values_list('title', flat=True))
    incl = list(AcceptedList.objects.values_list('title', flat=True))

    excl_filter = partial(is_not_excl, excl)
    incl_filter = partial(is_incl, incl)

    items = \
        filter(incl_filter,
               filter(excl_filter,
                      map(get_link_title_desc,
                          filter(is_new_job,
                                 join(
                                     map(get_rss_items, job_feeds))))))

    for x in items:
        save_job(x)


class Command(BaseCommand):
    args = 'no arguments!'
    help = u'News import from external resources'

    def handle(self, *args, **options):
        """
        Основной метод - точка входа
        """
        import_jobs()
