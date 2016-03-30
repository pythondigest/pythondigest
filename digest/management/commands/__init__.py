# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pickle
import re

import requests
from readability import Document

try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen

from bs4 import BeautifulSoup

from digest.models import Item, Section
from django.conf import settings
from pygoogle import pygoogle
from pygoogle.pygoogle import PyGoogleHttpException
import datetime
from time import sleep
from stem import control, Signal, stem
from django.core.management import call_command


def parse_weekly_digest(item_data):
    if 'Python Weekly' in item_data.get('title'):
        call_command('import_python_weekly', item_data.get('link'))


def is_weekly_digest(item_data):
    title = item_data.get('title')
    return bool(
        'Python Weekly' in title
    )


def _clojure_get_youtube_urls_from_page():
    """
    Замыкание
    Возвращает функцию, которая по коду страницы (requests.text)
        возвращает youtube ссылку
        Применяется для раздела Видео
    :return:
    """
    reg_list = '((https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(watch\?.*?(?=v=)v=|embed/|v/|.+\?v=)?([^&=%\?]{11}))'

    youtube_links = ['youtu.be', 'youtube.com', 'youtube-nocookie.com']

    def form_url(url):
        result = url
        _ = re.findall(reg_list, url)
        if _ and len(_) == 1 and len(_[0]) == 7:
            result = "https://www.youtube.com/watch?v=%s" % _[0][6]
        return result

    def clean_urls(url):
        result = None
        url = re.sub(r'<[^<]+?>', '', url)
        if any(x in url for x in youtube_links):
            result = url.replace(r'//', '') if url.startswith('//') else url
        return result

    def parse_page(content):

        result = None
        try:
            a = filter(lambda x: "youtu" in x, content.split('\n'))
            urls = []
            for x in a:
                _ = re.findall(reg_list, x)
                if _:
                    urls.extend([x[0] for x in filter(lambda x: x and len(x) > 1 and x[0], _)])
                    break

            result = list(
                set(
                    map(form_url,
                        map(clean_urls,
                            filter(lambda x: '%2F' not in x, urls)))))[0]
        except Exception:
            raise
        finally:
            return result

    return parse_page


get_youtube_url_from_page = _clojure_get_youtube_urls_from_page()


def _date_to_julian_day(my_date):
    """
    Returns the Julian day number of a date.
    Origin: http://code-highlights.blogspot.ru/2013/01/julian-date-in-python.html
    :param my_date:
    :return:
    """
    a = (14 - my_date.month) // 12
    y = my_date.year + 4800 - a
    m = my_date.month + 12 * a - 3
    return my_date.day + \
           ((153 * m + 2) // 5) + \
           365 * y + \
           y // 4 - \
           y // 100 + \
           y // 400 - \
           32045


def _get_http_data_of_url(url: str):
    """
    Возвращает http-статус, текст новости по url
    В случае не успеха - '404', None
    :param url:
    :return:
    """

    try:
        assert isinstance(url, str), 'Not valid url: %s, type (%s)' % \
                                     (url, type(url))
        r = requests.get(url)
        readable_article = Document(r.content).summary()
        status_code = str(r.status_code)
        result = status_code, readable_article, r.text

    except (requests.ConnectionError, AssertionError) as e:
        result = str(404), None, None
    return result


def _get_tags_for_item(item_data: dict, tags_names: list):
    """

    item_data - словарь.
    tags_names - list строк

    значения в словаре item_data, если значение строка
        то сплитится о пробелу и сравнивается с каждым тегом
        если совпадает, то возвращает совпадение

    :param item_data:
    :param tags_names:
    :return:
    """

    try:
        assert isinstance(item_data, dict)
        assert isinstance(tags_names, list)
        return_tags = []
        for _, value in item_data.items():
            if isinstance(value, str) and value:
                return_tags.extend([tag for tag in tags_names
                                    if (tag.lower() in value.lower())])
        result = list(set(return_tags))
    except AssertionError:
        result = []
    return result


def renew_connection():
    with control.Controller.from_port(port=9051) as ctl:
        ctl.authenticate(settings.TOR_CONTROLLER_PWD)
        ctl.signal(Signal.NEWNYM)
        sleep(5)


def fresh_google_check(link: str, attempt=5, debug=False):
    """Проверяет, индексировался ли уже ресурс гуглом раньше.

    чем за 2 недели до сегодня.
    :param link:
    :param attempt:
    :return:

    """
    if debug:
        return False
    try:
        assert isinstance(link, str)
        today = datetime.date.today()
        date_s = _date_to_julian_day(today - datetime.timedelta(days=365 * 8))
        date_e = _date_to_julian_day(today - datetime.timedelta(days=7 * 2))
        query = u'site:%s daterange:%s-%s' % (link, date_s, date_e,)

        result = False
        for i in range(0, attempt):
            g = pygoogle(query.encode('utf-8'),
                         raise_http_exceptions=True,
                         proxies=settings.PROXIES_FOR_GOOGLING)

            try:
                result = bool(g.get_result_count())
            except PyGoogleHttpException as e:
                renew_connection()
                continue
            break
    except (AssertionError, PyGoogleHttpException, stem.SocketError):
        result = False

    return result


def get_tweets_by_url(base_url: str):
    url = urlopen(base_url)
    soup = BeautifulSoup(url, 'lxml')
    http_code = url.getcode()
    url.close()

    result = []
    for p in soup.findAll('p', 'tweet-text'):
        try:
            tw_lnk = p.find('a', 'twitter-timeline-link').get(
                'data-expanded-url')
            tw_text = p.contents[0]
            result.append([tw_text, tw_lnk, http_code])
        except:
            pass
    return result


# -------------------
# -------------------
# -------------------
# -------------------
# -------------------
# -------------------


def _check_if_action(if_action: str, if_item: str, if_value: str):
    pattern = re.compile(if_value) if if_action == 'regex' else None
    return (if_action == 'not_equal' and if_item != if_value) or \
           (if_action == 'contains' and if_value in if_item) or \
           (if_action == 'equal' and if_item == if_value) or \
           (pattern is not None and pattern.search(
               if_item) is not None)


def _make_then_action(then_action, rules, sections, statuses, tags):
    query_rules = rules
    query_sections = sections
    query_statuses = statuses
    tags_names = tags

    # ---------------------
    def _make_then_action_set(then_element: str, then_value: str):
        result = {}
        if (then_element == 'status' and then_value in query_statuses) or \
                (then_element == 'section' and query_sections.filter(
                    title=then_value).exists()):
            result = {then_element: then_value}

        if then_element == 'http_code' and then_value == '404':
            result = {'status': 'moderated'}

        if then_element in ['title', 'description'] and then_value:
            result = {then_element: then_value}

        return result

    # ---------------------

    def _make_then_action_add(then_element: str, then_value: str):
        result = {}
        if then_element == 'tags' and then_value in tags_names:
            result = {then_element: then_value}

        return result

    # ---------------------

    def _make_then_action_remove_sub_string(then_element: str, then_value: str,
                                            if_item: str):
        result = {}

        if then_element in ['title', 'description'] and then_value:
            result = {then_element: if_item.replace(then_value, '')}

        return result

    # ---------------------

    functions = {
        'set': _make_then_action_set,
        'add': _make_then_action_add,
        'remove': _make_then_action_remove_sub_string,
    }

    return functions.get(then_action)


def apply_video_rules(item_data: dict):
    """
    Применяем правила (захардкоженые) для раздела Видео
    В данном случае если раздел видео, то пытаемся выдрать ссылку на видео
    :param item_data:
    :return:
    """
    youtube_links = ['youtu.be', 'youtube.com', 'youtube-nocookie.com']

    result = item_data
    if item_data.get('section') == Section.objects.get(title='Видео') \
            and all(x not in item_data.get('link') for x in youtube_links) \
            and 'raw_content' in item_data:
        url = get_youtube_url_from_page(item_data.get('raw_content'))
        if url is not None:
            item_data['additionally'] = url
    return result


def apply_parsing_rules(item_data: dict, query_rules, query_sections,
                        query_statuses, query_tags):
    # tags_names = list(query_tags.values_list('name', flat=True))
    tags_names = []
    data = {}

    # _tags_of_item = _get_tags_for_item(item_data, tags_names)
    # if _tags_of_item:
    #     data['tags'] = list(_tags_of_item)

    for rule in query_rules.order_by('-weight'):
        if rule.then_element == 'status' and \
                (data.get('status') == 'moderated' or
                         data.get('status') == 'active'):
            continue
        if rule.then_element == 'section' and 'section' in data:
            continue

        if_item = item_data.get(rule.if_element, None)
        if if_item is not None:
            if _check_if_action(rule.if_action, if_item, rule.if_value):
                then_element = rule.then_element
                then_action = rule.then_action
                then_value = rule.then_value

                function = _make_then_action(then_action, query_rules,
                                             query_sections, query_statuses,
                                             tags_names)
                if then_action == 'set':
                    data.update(function(then_element, then_value))
                elif then_action == 'remove':
                    data.update(function(then_element, then_value, if_item))
                elif then_action == 'add':
                    if then_element in data:
                        data[then_element].extend(
                            list(function(then_element, then_value).get(
                                then_element, [])))
                    else:
                        data[then_element] = list(function(then_element,
                                                           then_value)
                                                  .get(then_element, []))

    # исключений не должно быть,
    # ибо по коду везде очевидно что объект сущесвтует
    # но пускай будет проверка на существование
    if 'section' in data:
        try:
            data['section'] = query_sections.get(title=data.get('section'))
        except Exception:
            pass
    if 'tags' in data:
        _tags = []
        data['tags'] = list(set(data['tags']))
        for x in data['tags']:
            try:
                _tags.append(query_tags.get(name=x))
            except Exception:
                pass
        data['tags'] = _tags
    return data


# -------------------
# -------------------
# -------------------
# -------------------


def save_item(item):
    assert 'title' in item
    assert 'resource' in item
    assert 'link' in item

    if not Item.objects.filter(title=item.get('title'),
                               link=item.get('link'),
                               description=item.get('description')).exists():
        _a = Item(
            title=item.get('title'),
            resource=item.get('resource'),
            link=item.get('link'),
            description=item.get('description', ''),
            status=item.get('status', 'autoimport'),
            user_id=settings.BOT_USER_ID,
            section=item.get('section', None),
            additionally=item.get('additionally', None),
            language=item.get('language') if item.get('language') else 'en')

        _a.save()

        if item.get('tags'):
            _a.tags.add(*item.get('tags'))
            _a.save()
        elif item.get('status') == 'active':
            _a.save()

def save_pickle_file(filepath, data):
    with open(filepath, 'wb') as fio:
        pickle.dump(data, fio)


def load_pickle_file(filepath):
    with open(filepath, 'rb') as fio:
        return pickle.load(fio)
