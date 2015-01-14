# coding=utf-8
import datetime
import pytils
from django.contrib.syndication.views import Feed
from digest.models import Item, Issue


class CommonFeed(Feed):
    """
    Лента РСС для новостей
    """
    title = u"Дайджест новостей о python"
    link = "/"
    description = u"""Рускоязычные анонсы свежих новостей о python и близлежащих технологиях."""

    @staticmethod
    def items():
        return Item.objects.filter(status='active').order_by('-modified_at')[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description

    def item_link(self, item):
        return item.link

    def item_pubdate(self, item):
        return item.modified_at

class AllEntriesFeed(CommonFeed):
    pass

class TwitterEntriesFeed(CommonFeed):
    """
    Лента РСС для twitter
    """
    def item_link(self, item):
        return item.internal_link


class RussianEntriesFeed(CommonFeed):
    """
    Лента РСС для русскоязычных новостей
    """
    description = u"""Рускоязычные анонсы свежих новостей о python и близлежащих технологиях (только русскоязычные материалы)."""

    def item_link(self, item):
        return item.internal_link

    @staticmethod
    def items():
        return Item.objects.filter(status='active', language='ru').order_by('-modified_at')[:10]


class IssuesFeed(CommonFeed):
    """
    Лента РСС для выпусков новостей
    """
    title = u"Дайджест новостей о python - все выпуски"
    link = "/issues/"
    description = u"""Рускоязычные анонсы свежих новостей о python и близлежащих технологиях."""

    @staticmethod
    def items():
        return Issue.objects.filter(status='active').order_by('-published_at')[:10]

    def item_title(self, item):
        df = pytils.dt.ru_strftime(u'%d %B %Y', item.date_from, inflected=True)
        dt = pytils.dt.ru_strftime(u'%d %B %Y', item.date_to, inflected=True)
        return u'''Python-digest #%s. Новости, интересные проекты,
        статьи и интервью [%s — %s]''' % (item.pk, df, dt)

    def item_pubdate(self, item):
        return datetime.datetime.combine(item.published_at, datetime.time(0,0,0))