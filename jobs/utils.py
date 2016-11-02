# -*- encoding: utf-8 -*-
import logging
from textwrap import wrap

import requests
from django.conf import settings
from django.utils.dateparse import parse_datetime
from typing import Dict

from jobs.signals import sig_integration_failed

logger = logging.getLogger(__name__)

USER_AGENT = 'pydigest.ru/%s (pydigest@gmail.com)' % '.'.join(
    map(str, settings.VERSION))


def format_currency(val):
    """Форматирует значение валюты, разбивая его кратно
    тысяче для облегчения восприятия.
    :param val:
    :return:
    """
    return ' '.join(wrap(str(int(val))[::-1], 3))[::-1]


def get_from_url(url: str):
    """Возвращает объект ответа requests с указанного URL.
    :param str url:
    :return:
    """
    r_kwargs = {
        'allow_redirects': True,
        'headers': {'User-agent': USER_AGENT},
    }
    return requests.get(url, **r_kwargs)


def get_json(url: str) -> Dict:
    """Возвращает словарь, созданный из JSON документа, полученного
    с указанного URL.
    :param str url:
    :return:
    """

    result = {}
    try:
        response = get_from_url(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        sig_integration_failed.send(
            None,
            description='URL %s. Error: %s' % (url, e)
        )
    else:
        try:
            result = response.json()
        except ValueError as e:
            err_msg = 'Not found JSON with ({0}) vacancies: {1}'
            logger.error(err_msg.format(url, e))
    return result


class HhVacancyManager(object):
    """Объединяет инструменты для работы с вакансиями с hh.ru."""

    @classmethod
    def get_status(cls, url):
        """Возвращает состояние вакансии по указанному URL.
        :param url:
        :return:
        """
        response = get_json(url)
        return response['archived'] if response else None

    @classmethod
    def fetch_list(cls):
        """Возвращает словарь с данными вакансий, полученный из внешнего
        источника.
        :return:
        """
        base_url = 'https://api.hh.ru/vacancies/'
        query = (
            'search_field=%(field)s&per_page=%(per_page)s'
            '&order_by=publication_time&period=1&text=%(term)s' % {
                'term': 'python',
                'per_page': 500,
                'field': 'name',  # description
            })

        response = get_json('%s?%s' % (base_url, query))

        if 'items' not in response:
            return None

        results = []
        for item in response['items']:
            salary_from = salary_till = salary_currency = ''

            if item['salary']:
                salary = item['salary']
                salary_from = salary['from']
                salary_till = salary['to']
                salary_currency = salary['currency']

            employer = item['employer']
            url_logo = employer['logo_urls']
            if url_logo:
                url_logo = url_logo['90']

            results.append({
                '__archived': item['archived'],
                'src_id': item['id'],
                'src_place_name': item['area']['name'],
                'src_place_id': item['area']['id'],
                'title': item['name'],
                'link': item['alternate_url'],
                'url_api': item['url'],
                'url_logo': url_logo,
                'employer_name': employer['name'],
                'salary_from': salary_from or None,
                'salary_till': salary_till or None,
                'salary_currency': salary_currency,
                'published_at': parse_datetime(item['published_at']),
            })

        return results
