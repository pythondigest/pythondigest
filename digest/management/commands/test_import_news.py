# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand

import feedparser
from bs4 import BeautifulSoup
from digest.management.commands import fresh_google_check
from digest.management.commands.import_news import _get_http_data_of_url, \
    apply_parsing_rules, parsing
from digest.models import AutoImportResource, Item

try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen


def get_tweets():
    """Импорт твитов пользователя."""
    dsp = []
    for src in AutoImportResource.objects.filter(type_res='twitter',
                                                 in_edit=True):
        url = urlopen(src.link)
        soup = BeautifulSoup(url)
        url.close()

        num = 0

        print('\n\n' + '=' * 25)
        print('  ' + src.name)
        print('=' * 25 + '\n')
        resource = src.resource
        excl = src.excl.split(', ')
        print('Исключения:')
        print('-' * 25)
        for i in excl:
            print(i)
        print('\n')
        print('Распарсенные твитты:')
        print('-' * 25)
        for p in soup.findAll('p', 'ProfileTweet-text js-tweet-text u-dir'):
            try:
                tw_lnk = p.find('a', 'twitter-timeline-link').get(
                    'data-expanded-url')

                for i in excl:
                    if tw_lnk.find(i) > -1 and i != '':
                        excl_link = True
                    else:
                        excl_link = False

                if not excl_link and p.contents[0].find(src.incl) > -1:
                    num = num + 1
                    tw_txt = p.contents[0].replace(src.incl, '')
                    print(str(num) + '. excl:' + str(excl_link) + ' ' + tw_txt
                          + '---  ' + tw_lnk)
                    dsp.append([tw_txt, tw_lnk, resource])
            except:
                pass
        print('-' * 25)
    return dsp


def get_rss(**kwargs):
    for src in AutoImportResource.objects.filter(type_res='rss',
                                                 in_edit=False):
        print('\n\n' + '=' * 25)
        print('  ' + src.name)
        print('=' * 25 + '\n')

        num = 0
        rssnews = feedparser.parse(src.link)
        for n in rssnews.entries:

            title = u'[!] %s' % n.title if fresh_google_check(
                n.title,
                debug=True) else n.title

            http_code, content, _ = _get_http_data_of_url(n.link)

            item_data = {
                'title': title,
                'link': n.link,
                'http_code': http_code,
                'content': content,
                'description': n.summary,
                'resource': src.resource,
            }
            data = apply_parsing_rules(item_data, **kwargs) if kwargs.get(
                'query_rules') else {}
            item_data.update(data)

            print_str = ''
            print_str += 'status: %s' % item_data['status'] if (
                'status' in item_data) else ''
            print_str += 'tags: %s' % item_data['tags'] if ('tags' in
                                                            item_data) else ''
            print_str += 'section: %s' % item_data['section'] if (
                'section' in item_data) else ''
            print(print_str)
            try:
                lastnews = Item.objects.get(link=item_data.get('link'))
            except Item.DoesNotExist:
                num += 1
                print('%d: Title: %s (%s)' %
                      (num, item_data.get('title'), item_data.get('link')))
                # print src.resource


class Command(BaseCommand):

    args = 'no arguments!'
    help = u''

    def handle(self, *args, **options):
        '''
        Основной метод - точка входа
        '''
        print(get_tweets())
        print(parsing(get_rss))
