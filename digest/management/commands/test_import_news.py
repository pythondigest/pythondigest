# -*- coding: utf-8 -*-
from urllib import urlopen

import feedparser
from django.core.management.base import BaseCommand
from bs4 import BeautifulSoup

from digest.models import AutoImportResource, Item, ParsingRules, \
    ITEM_STATUS_CHOICES, Section
import requests

def get_tweets():
    '''
    Импорт твитов пользователя
    '''
    dsp = []
    for src in AutoImportResource.objects.filter(type_res='twitter', in_edit=True):
        url = urlopen( src.link )
        soup = BeautifulSoup( url )
        url.close()

        num = 0
        
        print '\n\n' + '='*25
        print '  ' + src.name
        print '='*25 + '\n'
        resource = src.resource
        excl = src.excl.split(', ')
        print 'Исключения:'
        print '-'*25
        for i in excl:
            print i
        print '\n'
        print 'Распарсенные твитты:'
        print '-'*25
        for p in soup.findAll('p', 'ProfileTweet-text js-tweet-text u-dir'):
            try:
                tw_lnk = p.find('a', 'twitter-timeline-link').get('data-expanded-url')
                
                for i in excl:
                    if tw_lnk.find(i) > -1 and i <> '':
                        excl_link=True
                    else:
                        excl_link = False
                
                if not excl_link and p.contents[0].find(src.incl) > -1:
                    num = num + 1
                    tw_txt = p.contents[0].replace(src.incl, '')
                    print str(num) + '. excl:' + str(excl_link) + ' ' + tw_txt + '---  ' + tw_lnk
                    dsp.append([tw_txt, tw_lnk, resource])
            except:
                pass
        print '-'*25
    return dsp


def _get_http_code(url):
    try:
        r = requests.head(url)
        result = r.status_code
    except requests.ConnectionError:
        result = 404
    return result


def _apply_parsing_rules(entry, rules, sections, statuses):
    item_data = {
        'item_title': entry.title,
        'item_url': entry.link,
        # 'http_code': _get_http_code(entry.link),
    }
    data = {}

    for rule in rules:
        if rule.then_element == 'status' and (data.get('status') == 'moderated' or data.get('status') == 'active'):
            continue
        if rule.then_element == 'category' and 'category' in data:
            continue

        if_item = item_data.get(rule.if_element, None)
        if if_item is not None:
            if_action = rule.if_action
            if_value = rule.if_value

            if (if_action == 'not_equal' and if_item != if_value) or \
                    (if_action == 'contains' and if_value in if_item) or \
                    (if_action == 'equal' and if_item == if_value):
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
    return data


def get_rss():
    rules = ParsingRules.objects.all()
    sections = Section.objects.all()
    item_statuses = [x[0] for x in ITEM_STATUS_CHOICES]
    for src in AutoImportResource.objects.filter(type_res='rss', in_edit=False):
        print '\n\n' + '='*25
        print '  ' + src.name
        print '=' * 25 + '\n'

        num = 0
        rssnews = feedparser.parse(src.link)
        for n in rssnews.entries:
            if rules:
                data = _apply_parsing_rules(n, rules, sections, item_statuses)
                print(data)
            try:
                lastnews = Item.objects.get(link = n.link)
            except Item.DoesNotExist:
                num += 1
                print '%d: Title: %s (%s)' % (num, n.title, n.link)
                # print src.resource


class Command(BaseCommand):
    
    args = 'no arguments!'
    help = u''

    def handle(self, *args, **options):
        '''
        Основной метод - точка входа
        '''
        print get_tweets()
        print get_rss()
        
