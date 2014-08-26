# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from urllib import urlopen
from BeautifulSoup import BeautifulSoup
from digest.models import AutoImportResource, Item

def get_tweets():
    '''
    Импорт твитов пользователя
    '''
    dsp = []
    for src in AutoImportResource.objects.filter(type_res='twitter', in_edit=False):

        url = urlopen( src.link )
        soup = BeautifulSoup( url )
        url.close()

        num = 0

        resource = src.resource
        excl = src.excl.split(', ')

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
                    dsp.append([tw_txt, tw_lnk, resource])
            except:
                pass

    return dsp



class Command(BaseCommand):
    
    args = 'no arguments!'
    help = u''

    def handle(self, *args, **options):
        '''
        Основной метод - точка входа
        '''
        for i in get_tweets():
            
            try:
                lastnews = Item.objects.get(link = i[1])
                #print 'Not add: ' + i[0]
            except Item.DoesNotExist:
                #print 'Add: ' + i[0]
                R = Item(
                        title = i[0],
                        resource = i[2],
                        link = i[1],
                        status = 'autoimport',
                    )
                R.save()