# -*- coding: utf-8 -*-
from django.db import transaction
from datetime import datetime
import feedparser

from .models import ResourceRSS, RawItem


def update_rss():
    for res in ResourceRSS.objects.filter(status=True):
        try:
            data = feedparser.parse(res.link)
        except Exception as e:
            print ('sync failed: %s' % e)
            continue

        print res.link
        print data.feed.keys()
        if 'updated_parsed' not in data.feed.keys():
            updated_date = to_datetime(data.entries[0].published_parsed)
        else:
            updated_date = to_datetime(data.entries[0].updated_parsed)

        if res.sync_date and res.sync_date >= updated_date:
            continue

        with transaction.commit_on_success():
            for item in data.entries:
                #NOTE need exist published in item like
                # if not 'published_parsed':
                #     related_to_date=datetime.now()

                item = RawItem.objects.filter(link=item.link).count()
                if item:
                    continue

                entry = RawItem(
                    title=item.title,
                    resource_rss=res,
                    description=item.title,
                    link=item.link,
                    language=res.language,
                    related_to_date=to_datetime(item.published_parsed),
                )
                if res.sync_date and res.sync_date > entry.related_to_date:
                    continue

                entry.save()
            res.sync_date = updated_date
            res.save()
            print ('sync rss "%s" done!' % data.feed.title)

def to_datetime(feed_date):
    return datetime(*(feed_date[0:6]))
