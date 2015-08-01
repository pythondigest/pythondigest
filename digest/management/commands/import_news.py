# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re

import feedparser
from django.core.management.base import BaseCommand
from readability import Document
import requests

import digest

try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen


from bs4 import BeautifulSoup

from digest.models import AutoImportResource, Item, ParsingRules, Section, \
    ITEM_STATUS_CHOICES, Tag
from django.conf import settings
from pygoogle import pygoogle
from pygoogle.pygoogle import PyGoogleHttpException
import datetime
from time import sleep, mktime
import stem
from stem import control


def _get_http_data(url):
    try:
        r = requests.get(url)
        readable_article = Document(r.content).summary()
        status_code = str(r.status_code)
        result = status_code, readable_article
    except requests.ConnectionError:
        result = str(404), None
    return result


def _apply_parsing_rules(item_data, query_rules, query_sections, query_statuses,
                         query_tags):
    tags_names = [x.name for x in query_tags.all()]
    data = {}
    for rule in query_rules:
        if rule.then_element == 'status' and \
                (data.get('status') == 'moderated' or
                         data.get(
                    'status') == 'active'):
            continue
        if rule.then_element == 'section' and 'section' in data:
            continue

        if_item = item_data.get(rule.if_element, None)
        if if_item is not None:
            if_action = rule.if_action
            if_value = rule.if_value
            pattern = re.compile(if_value) if if_action == 'regex' else None

            if (if_action == 'not_equal' and if_item != if_value) or \
                    (if_action == 'contains' and if_value in if_item) or \
                    (if_action == 'equal' and if_item == if_value) or \
                    (pattern is not None and pattern.search(
                        if_item) is not None):
                then_element = rule.then_element
                then_action = rule.then_action
                then_value = rule.then_value

                if ((
                            then_element == 'status' and then_value in query_statuses) or \
                            (
                                    then_element == 'section' and query_sections.filter(
                                title=then_value).exists())
                    ):
                    if then_action == 'set':
                        data[then_element] = then_value
                if then_element == 'tags' and then_value in tags_names:
                    if then_action == 'add':
                        try:
                            data[then_element].append(then_value)
                        except KeyError:
                            data[then_element] = [then_value]
                elif then_element == 'http_code':
                    data['status'] = 'moderated'

    # исключений не должно быть,
    # ибо по коду везде очевидно что объект сущесвтует
    # но пускай будет проверка на существование
    if 'section' in data:
        try:
            data['section'] = query_sections.get(
                title=data.get('section'))
        except digest.models.DoesNotExist:
            pass
    if 'tags' in data:
        _tags = []
        for x in data['tags']:
            try:
                _tags.append(query_tags.get(name=x))
            except digest.models.DoesNotExist:
                pass
        data['tags'] = _tags
    return data


def time_struct_to_datetime(time_struct):
    timestamp = mktime(time_struct)
    dt = datetime.datetime.fromtimestamp(timestamp)
    return dt


def get_tweets():
    '''
    Импорт твитов пользователя
    '''
    dsp = []
    for src in AutoImportResource.objects.filter(type_res='twitter', in_edit=False):
        url = urlopen(src.link)
        soup = BeautifulSoup(url)
        http_code = url.getcode()
        url.close()

        resource = src.resource
        excl = [s for s in (src.excl or '').split(',') if s]

        for p in soup.findAll('p', 'tweet-text'):
            try:
                tw_lnk = p.find('a', 'twitter-timeline-link').get('data-expanded-url')
                tw_text = p.contents[0]

                excl_link = bool([i for i in excl if i in tw_lnk])

                if not excl_link and src.incl in tw_text:
                    tw_txt = tw_text.replace(src.incl, '')
                    dsp.append([tw_txt, tw_lnk, resource, http_code])
            except:
                pass

    return dsp


def parsing(func):
    data = {'query_rules': ParsingRules.objects.all(),
            'query_sections': Section.objects.all(),
            'query_tags': Tag.objects.all(),
            'query_statuses': [x[0] for x in ITEM_STATUS_CHOICES]
            }
    func(**data)


def save_new_tweets(**kwargs):
    for i in get_tweets():
        ct = len(Item.objects.filter(link=i[1])[0:1])
        if ct:
            continue

        title = i[0]
        if fresh_google_check(i[1]):
            title = u'[!] %s' % title

        data = {}
        if kwargs.get('rules'):
            item_data = {
                'item_title': title,
                'item_url': i[1],
                'http_code': i[3]
            }
            data = _apply_parsing_rules(item_data, **kwargs)

        _a = Item(
            title=title,
            resource=i[2],
            link=i[1],
            section=data.get('section', None),
            status=data.get('status', 'autoimport'),
            user_id=settings.BOT_USER_ID
        )

        _a.save()
        if data.get('tags'):
            _a.tags.add(*data.get('tags'))
            _a.save()


def import_rss(**kwargs):
    for src in AutoImportResource.objects.filter(type_res='rss', in_edit=False):

        rssnews = feedparser.parse(src.link)
        today = datetime.date.today()
        week_before = today - datetime.timedelta(weeks=1)
        for n in rssnews.entries:
            ct = len(Item.objects.filter(link=n.link)[0:1])
            if ct:
                continue

            time_struct = getattr(n, 'published_parsed', None)
            if time_struct:
                dt = time_struct_to_datetime(time_struct)
                if dt.date() < week_before:
                    continue

            title = n.title
            if fresh_google_check(n.link):
                title = u'[!] %s' % title

            data = {}
            section = None
            if kwargs.get('query_rules'):
                http_code, content = _get_http_data(n.link)

                item_data = {
                    'item_title': title,
                    'item_url': n.link,
                    'http_code': http_code,
                    'item_content': content,
                    'item_description': n.summary,
                }
                data = _apply_parsing_rules(item_data, **kwargs)

            _a = Item(
                title=title,
                resource=src.resource,
                link=n.link,

                status=data.get('status', 'autoimport'),
                user_id=settings.BOT_USER_ID,
                section=data.get('section', None),
                language=src.language if src.language else 'en'
            )

            _a.save()
            if data.get('tags'):
                _a.tags.add(*data.get('tags'))
                _a.save()

def renew_connection():
    with control.Controller.from_port(port=9051) as ctl:
        ctl.authenticate(settings.TOR_CONTROLLER_PWD)
        ctl.signal(stem.Signal.NEWNYM)
        sleep(5)

def fresh_google_check(link, attempt=0):
    '''
    Проверяет, индексировался ли уже ресурс гуглом раньше
    чем за 2 недели до сегодня.
    '''
    today = datetime.date.today()
    date_s = date_to_julian_day( today - datetime.timedelta(days=365 * 8) )
    date_e = date_to_julian_day( today - datetime.timedelta(days=7 * 2) )
    query = u'site:%s daterange:%s-%s' % (link, date_s, date_e,)

    res = False
    for i in range(0, 5):
        g = pygoogle(
            query.encode('utf-8'),
            raise_http_exceptions=True,
            proxies=settings.PROXIES_FOR_GOOGLING
        )

        try:
            res = bool(g.get_result_count())
        except PyGoogleHttpException as e:
            renew_connection()
            continue
        break

    return res


def date_to_julian_day(my_date):
    '''
    Returns the Julian day number of a date.
    Origin: http://code-highlights.blogspot.ru/2013/01/julian-date-in-python.html
    '''
    a = (14 - my_date.month)//12
    y = my_date.year + 4800 - a
    m = my_date.month + 12*a - 3
    return my_date.day + ((153*m + 2)//5) + 365*y + y//4 - y//100 + y//400 - 32045


class Command(BaseCommand):
    
    args = 'no arguments!'
    help = u'News import from external resources'

    def handle(self, *args, **options):
        '''
        Основной метод - точка входа
        '''
        # parsing(save_new_tweets)
        parsing(import_rss)
