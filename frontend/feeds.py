# coding=utf-8
from django.contrib.syndication.views import Feed
from digest.models import Item


class LatestEntriesFeed(Feed):
    """
    Лента РСС для новостей
    """
    title = u"Дайджест новостей о python"
    link = "/"
    description = u"""Новости собираются с мира по нитке на совершенно безвозмезной основе. Ты легко можешь
    посодействовать проекту добавив ссылку на интересную новость, статью, интервью или проект о python. А еще можно
    форкнуть код этого проекта на Github и помочь в развитии его функциональности."""

    @staticmethod
    def items():
        return Item.objects.filter(status='active').order_by('-created_at')[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description

    def item_link(self, item):
        return item.link