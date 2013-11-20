from celery.task import task
from django.db import transaction
from datetime import datetime
from time import mktime
import feedparser

from .models import ResourceRSS, RawItem

@task
def update_rss():
    for resource in ResourceRSS.objects.filter(status=True):
        try:
            data = feedparser.parse(resource.link)
            if 'updated_parsed' not in data.feed.keys():
                updated_date = datetime.fromtimestamp(mktime(data.entries[0].published_parsed))
            else:
                updated_date = datetime.fromtimestamp(mktime(data.entries[0].updated_parsed))
            if not resource.sync_date or resource.sync_date < updated_date:
                with transaction.commit_on_success():
                    for item in data.entries:
                        #NOTE need exist published in item like
                        # if not 'published_parsed':
                        #     related_to_date=datetime.now()
                        entry = RawItem(
                                title=item.title,
                                description=item.title,
                                link=item.link,
                                related_to_date=datetime.fromtimestamp(\
                                                mktime(item.published_parsed)),
                        )
                        if entry and (not resource.sync_date or \
                                     entry.related_to_date > resource.sync_date):
                            entry.save()
                resource.sync_date = updated_date
                resource.save()
                print ('sync rss "%s" done!' % data.feed.title)
        except Exception as e:
            print ('sync failes: %s' % e)
