# coding=utf-8
import datetime
from django.contrib.syndication.views import Feed
from digest.models import Item


class LatestEntriesFeed(Feed):
    """
    Лента РСС для новостей
    """
    title = u"Дайджест новостей о python"
    link = "/"
    description = u"""Рускоязычные анонсы свежих новостей о python и близлежащих технологиях."""

    @staticmethod
    def items():
        return Item.objects.filter(status='active').order_by('-created_at')[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description

    def item_link(self, item):
        return item.link
        
    def item_pubdate(self, item):
        return datetime.datetime.combine(item.created_at, datetime.time(0,0,0))
