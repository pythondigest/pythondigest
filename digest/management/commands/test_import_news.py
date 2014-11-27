# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from urllib import urlopen
from BeautifulSoup import BeautifulSoup
from digest.models import AutoImportResource

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


def get_rss():
    for src in AutoImportResource.objects.filter(type_res='rss', in_edit=True):
        print '\n\n' + '='*25
        print '  ' + src.name
        print '='*25 + '\n'
        
        
        num = 0
        rssnews = feedparser.parse(src.link)
        for n in rssnews.entries:
            try:
                lastnews = Item.objects.get(link = n.link)
            except Item.DoesNotExist:
                num += 1
                print '%d: Title: %s (%s)' % (num, n.title, n.link)
                print src.resource


class Command(BaseCommand):
    
    args = 'no arguments!'
    help = u''

    def handle(self, *args, **options):
        '''
        Основной метод - точка входа
        '''
        print get_tweets()
        print get_rss()
        
