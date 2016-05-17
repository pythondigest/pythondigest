# coding=utf-8
import datetime

import pytils
from django.conf import settings
from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Rss201rev2Feed

from digest.models import Issue, Item, Section


class DigestFeed(Feed):
    title = 'Дайджест новостей о python'
    link = '/'
    description = 'Рускоязычные анонсы свежих новостей о python и близлежащих технологиях.'

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description

    def item_link(self, item):
        return item.link

    def item_pubdate(self, item):
        return item.modified_at or item.activated_at


def mark_videos(query_set):
    video_section = Section.objects.filter(title="Видео")
    video_id = video_section.values_list('id', flat=True)[0]

    for x in query_set:
        if x.section is not None and x.section.id == video_id:
            x.title = "[Видео] %s" % x.title


class RawEntriesFeed(DigestFeed):
    @staticmethod
    def items():
        _ = Item.objects.filter(
            activated_at__lte=datetime.datetime.now(),
        ).order_by('-related_to_date')[:10]
        mark_videos(_)
        return _


class ItemDigestFeed(DigestFeed):
    """Лента РСС для новостей."""

    @staticmethod
    def items():
        _ = Item.objects.filter(
            status='active',
            activated_at__lte=datetime.datetime.now(),
        ).order_by(
            '-related_to_date')[:10]
        mark_videos(_)
        return _


class AllEntriesFeed(ItemDigestFeed):
    pass


class TwitterEntriesFeed(ItemDigestFeed):
    """Лента РСС для twitter."""

    def item_link(self, item):
        return item.internal_link


class RussianEntriesFeed(ItemDigestFeed):
    """Лента РСС для русскоязычных новостей."""
    description = 'Рускоязычные анонсы свежих новостей о python и близлежащих технологиях (только русскоязычные материалы).'

    def item_link(self, item):
        return item.internal_link

    @staticmethod
    def items():
        return Item.objects.filter(status='active',
                                   language='ru',
                                   activated_at__lte=datetime.datetime.now()).order_by(
            '-modified_at')[:10]


class CustomFeedGenerator(Rss201rev2Feed):
    def add_item_elements(self, handler, item):
        super(CustomFeedGenerator, self).add_item_elements(handler, item)
        handler.addQuickElement('image', item['image'])


class IssuesFeed(ItemDigestFeed):
    """Лента РСС для выпусков новостей."""
    title = 'Дайджест новостей о python - все выпуски'
    link = '/issues/'
    description = 'Рускоязычные анонсы свежих новостей о python и близлежащих технологиях.'

    feed_type = CustomFeedGenerator

    @staticmethod
    def items():
        return Issue.objects.filter(status='active').order_by(
            '-published_at')[:10]

    def item_title(self, item):
        df = pytils.dt.ru_strftime('%d %B %Y', item.date_from, inflected=True)
        dt = pytils.dt.ru_strftime('%d %B %Y', item.date_to, inflected=True)
        return 'Python-digest #%s. Новости, интересные проекты, статьи и интервью [%s — %s]' % (
        item.pk, df, dt)

    def item_pubdate(self, item):
        if item.published_at is not None:
            return datetime.datetime.combine(item.published_at,
                                             datetime.time(0, 0, 0))
        else:
            return item.published_at

    def item_extra_kwargs(self, obj):
        """
        Returns an extra keyword arguments dictionary that is used with
        the `add_item` call of the feed generator.
        Add the 'content' field of the 'Entry' item, to be used by the custom feed generator.
        """
        return {
            'image': 'http://' + settings.BASE_DOMAIN + obj.image.url if obj.image else ""}


class SectionFeed(DigestFeed):
    """Лента с категориями новостей."""
    section = 'all'

    def items(self):
        section = Section.objects.filter(title=self.section)
        if self.section == 'all' or len(section) != 1:
            result = Item.objects.filter(status='active',
                                         activated_at__lte=datetime.datetime.now()) \
                         .order_by('-related_to_date')[:10]
        else:
            result = Item.objects.filter(status='active',
                                         section=section[0],
                                         activated_at__lte=datetime.datetime.now()
                                         ).order_by(
                '-related_to_date')[:10]
        return result


class ItemVideoFeed(SectionFeed):
    section = 'Видео'


class ItemRecommendFeed(SectionFeed):
    section = 'Советуем'


class ItemNewsFeed(SectionFeed):
    section = 'Новости'


class ItemBookDocFeed(SectionFeed):
    section = 'Учебные материалы'


class ItemEventFeed(SectionFeed):
    section = 'Конференции, события, встречи разработчиков'


class ItemArticleFeed(SectionFeed):
    section = 'Статьи'


class ItemReleaseFeed(SectionFeed):
    section = 'Релизы'


class ItemPackagesFeed(SectionFeed):
    section = 'Интересные проекты, инструменты, библиотеки'


class ItemAuthorsFeed(SectionFeed):
    section = 'Колонка автора'
