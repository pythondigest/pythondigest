# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from functools import partial
from time import mktime
from datetime import datetime, date, timedelta

from django.core.management.base import BaseCommand
import feedparser

from funcy import join

from jobs.models import JobFeed, JobItem, RejectedList, AcceptedList
from jobs.utils import HhVacancyManager


def prepare_link_title(
        item: feedparser.FeedParserDict) -> feedparser.FeedParserDict:
    """
    Для RSS Item возвращает ссылку, заголовок и описание
    :param item:
    :return:
    """
    result = None
    if item:
        assert item.title, "Not found title in item"
        assert item.link, "Not found link in item"

        link = item.link.replace(u'https://www.google.com/url?rct=j&sa=t&url=',
                                 '')
        ge_ind = link.find('&ct=ga')
        if ge_ind > -1:
            link = link[0:ge_ind]
        title = item.title.replace('<b>', '').replace('</b>', '')
        item.link = link
        item.title = title
        result = item
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
    today = date.today()
    week_before = today - timedelta(weeks=1)
    time_struct = getattr(item, 'published_parsed', None)
    if time_struct:
        _timestamp = mktime(time_struct)
        dt = datetime.fromtimestamp(_timestamp)
        if dt.date() < week_before:
            result = False
    return result


def make_validate_dict(item: feedparser.FeedParserDict) -> dict:
    """
    Создает из RSS элемента словарь для сохранения.
    Метод пытается достать максимум информации из элемента
    :param item:
    :return:
    """
    _ = item.get('published_parsed', None)
    if _:
        published_at = datetime.fromtimestamp(mktime(_))
    else:
        published_at = datetime.now()

    try:
        result = {
            'title': item.title,
            'description': item.summary,
            'link': item.link,
            'published_at': published_at,
        }
    except Exception:
        result = {}
    return result


def is_not_excl(words: list, item: dict) -> bool:
    """
    Возвращает True если ни один из элементов item
    не содержит слов из списка на исключения
    :param words:
    :param item:
    :return:
    """
    return not bool([i for _, x in item.items() for i in words if i in str(x)])


def is_incl(words: list, item: dict) -> bool:
    """
    Возвращает True если хотя бы один элемент item
    :param words:
    :param item:
    :return:
    """
    for _, elem in item.items():
        for word in words:
            if word in str(elem):
                return True
    return False


def save_job(item: dict) -> None:
    """
    Функция для сохранения
    :param item:
    :return:
    """
    if not JobItem.objects.filter(link=item.get('link')).exists():
        JobItem(
            **item
        ).save()


def import_jobs_hh():
    """
    Импортрует вакансии с HH
    :return:
    """
    vacancies = HhVacancyManager.fetch_list()
    if not vacancies:
        return

    items = filter(lambda x: not x.pop('__archived', True), vacancies)

    for x in items:
        save_job(x)


def import_jobs_rss():
    _job_feeds_obj = JobFeed.objects.filter(in_edit=False, is_activated=True)
    job_feeds = list(_job_feeds_obj.values_list('link', flat=True))
    excl = list(RejectedList.objects.values_list('title', flat=True))
    incl = list(AcceptedList.objects.values_list('title', flat=True))

    excl_filter = partial(is_not_excl, excl)
    incl_filter = partial(is_incl, incl)

    items = \
        filter(incl_filter,
               filter(excl_filter,
                      map(make_validate_dict,
                          map(prepare_link_title,
                          filter(is_new_job,
                                 join(
                                     map(get_rss_items, job_feeds)))))))
    for x in items:
        save_job(x)


class Command(BaseCommand):
    args = 'no arguments!'
    help = u'News import from external resources'

    def handle(self, *args, **options):
        """
        Основной метод - точка входа
        """
        import_jobs_rss()
        import_jobs_hh()
