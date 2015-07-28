# -*- coding: utf-8 -*-
import feedparser
from django.core.management.base import BaseCommand

try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen


from bs4 import BeautifulSoup

from digest.models import AutoImportResource, Item
from django.conf import settings
from pygoogle import pygoogle
from pygoogle.pygoogle import PyGoogleHttpException
import datetime
from time import sleep, mktime
import stem
from stem import control


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
                    dsp.append([tw_txt, tw_lnk, resource])
            except:
                pass

    return dsp


def save_new_tweets():
    for i in get_tweets():
        ct = len(Item.objects.filter(link=i[1])[0:1])
        if ct:
            continue

        title = i[0]
        if fresh_google_check(i[1]):
            title = u'[!] %s' % title

        Item(
            title=title,
            resource=i[2],
            link=i[1],
            status='autoimport',
            user_id=settings.BOT_USER_ID,
        ).save()


def import_rss():
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

            Item(
                title=title,
                resource=src.resource,
                link=n.link,
                status='autoimport',
                user_id=settings.BOT_USER_ID,
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
