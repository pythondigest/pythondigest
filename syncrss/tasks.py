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
            data =feedparser.parse(resource.link)
            updated_date = datetime.fromtimestamp(mktime(data.feed.updated_parsed))
            if resource.sync_date < updated_date:
                with transaction.commit_on_success():
                    for item in data.entries:
                        print item.title
                        entry = RawItem(
                                title=item.title,
                                description=item.title,
                                link=item.link,
                                related_to_date=datetime.fromtimestamp(\
                                                mktime(item.updated_parsed)),
                        )
                        if entry and (not resource.sync_date or \
                                     entry.related_to_date > resource.sync_date):
                            entry.save()
                resource.sync_date = updated_date
                resource.save()
        except Exception as e:
            print ('sync failes: %s' % e)
