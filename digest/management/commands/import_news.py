# -*- coding: utf-8 -*-
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
    ITEM_STATUS_CHOICES
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
        status_code = r.status_code
        result = status_code, readable_article
    except requests.ConnectionError:
        result = 404, None
    return result


def _apply_parsing_rules(item_data, rules, sections, statuses):
    data = {}
    for rule in rules:
        if rule.then_element == 'status' and (
                        data.get('status') == 'moderated' or data.get(
                    'status') == 'active'):
            continue
        if rule.then_element == 'category' and 'category' in data:
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
                # then_action = rule.then_action
                then_value = rule.then_value

                # only set
                if (
                                then_element == 'status' and then_value in statuses) or \
                        (then_element == 'category' and sections.filter(
                            title=then_value).exists()):

                    data[then_element] = then_value

                elif then_element == 'http_code':
                    data['status'] = 'moderated'

    if 'category' in data:
        try:
            data['category'] = sections.get(
                title=data.get('category'))
        except digest.models.DoesNotExist:
            pass
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


def save_new_tweets():
    rules = ParsingRules.objects.all()
    sections = Section.objects.all()
    item_statuses = [x[0] for x in ITEM_STATUS_CHOICES]
    for i in get_tweets():
        ct = len(Item.objects.filter(link=i[1])[0:1])
        if ct:
            continue

        title = i[0]
        if fresh_google_check(i[1]):
            title = u'[!] %s' % title

        data = {}
        if rules:
            item_data = {
                'item_title': i[0],
                'item_url': i[1],
                'http_code': i[3]
            }
            data = _apply_parsing_rules(item_data, rules, sections,
                                        item_statuses)

        Item(
            title=title,
            resource=i[2],
            link=i[1],
            section=data.get('category', None),
            status=data.get('status', 'autoimport'),
            user_id=settings.BOT_USER_ID
        ).save()


def import_rss():
    rules = ParsingRules.objects.all()
    sections = Section.objects.all()
    item_statuses = [x[0] for x in ITEM_STATUS_CHOICES]
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

            data = {}
            section = None
            if rules:
                http_code, content = _get_http_data(n.link)

                item_data = {
                    'item_title': n.title,
                    'item_url': n.link,
                    'http_code': http_code,
                    'item_content': content,
                    'item_description': n.summary,
                }
                data = _apply_parsing_rules(item_data, rules, sections,
                                            item_statuses)

            title = n.title
            if fresh_google_check(n.link):
                title = u'[!] %s' % title

            Item(
                title=title,
                resource=src.resource,
                link=n.link,
                status=data.get('status', 'autoimport'),
                user_id=settings.BOT_USER_ID,
                section=data.get('category', None),
                language=src.language if src.language else 'en'
            ).save()

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
        save_new_tweets()
        import_rss()
