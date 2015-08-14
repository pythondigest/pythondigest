# coding=utf-8
import datetime

import pytils
from django.contrib.syndication.views import Feed

from digest.models import Item, Issue, Section


class DigestFeed(Feed):
    title = u"Дайджест новостей о python"
    link = "/"
    description = u"""Рускоязычные анонсы свежих новостей о python и близлежащих технологиях."""

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description

    def item_link(self, item):
        return item.link

    def item_pubdate(self, item):
        return item.modified_at


class ItemDigestFeed(DigestFeed):
    """
    Лента РСС для новостей
    """

    @staticmethod
    def items():
        return Item.objects.filter(status='active').order_by('-modified_at')[
               :10]


class AllEntriesFeed(ItemDigestFeed):
    pass


class TwitterEntriesFeed(ItemDigestFeed):
    """
    Лента РСС для twitter
    """
    def item_link(self, item):
        return item.internal_link


class RussianEntriesFeed(ItemDigestFeed):
    """
    Лента РСС для русскоязычных новостей
    """
    description = u"""Рускоязычные анонсы свежих новостей о python и близлежащих технологиях (только русскоязычные материалы)."""

    def item_link(self, item):
        return item.internal_link

    @staticmethod
    def items():
        return Item.objects.filter(status='active', language='ru').order_by('-modified_at')[:10]


class IssuesFeed(ItemDigestFeed):
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


class SectionFeed(DigestFeed):
    """
    Лента с категориями новостей
    """
    section = 'all'

    def items(self):
        section = Section.objects.filter(title=self.section)
        if self.section == 'all' or len(section) != 1:
            result = Item.objects.filter(status='active') \
                         .order_by('-modified_at')[:10]
        else:
            result = Item.objects.filter(status='active',
                                         section=section[0]).order_by(
                '-modified_at')[:10]
        return result

class ItemVideoFeed(SectionFeed):
    section = 'Видео'

class ItemRecommendFeed(SectionFeed):
    section = 'Советуем'

class ItemNewsFeed(SectionFeed):
    section = 'Новости'

class ItemBookDocFeed(SectionFeed):
    section = 'Книги и документация'

class ItemEventFeed(SectionFeed):
    section = 'Конференции, события, встречи разработчиков'

class ItemArticleFeed(SectionFeed):
    section = 'Статьи и интервью'

class ItemReleaseFeed(SectionFeed):
    section = 'Релизы'

class ItemPackagesFeed(SectionFeed):
    section = 'Интересные проекты, инструменты, библиотеки'
