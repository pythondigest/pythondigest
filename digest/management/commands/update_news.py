# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from random import shuffle

from django.core.management.base import BaseCommand

from digest.management.commands import _get_http_data_of_url, \
    _get_tags_for_item, load_pickle_file, save_pickle_file
from digest.models import Item, Tag


def diff(a, b):
    b = set(b)
    return [aa for aa in a if aa not in b]


def update_news():
    items_on_once = 10
    filepath = './pk_list.pickle'
    # если какая-то новость косячная, то на ней обработка не замнется
    pk_list = load_pickle_file(filepath)
    shuffle(pk_list)
    if pk_list is None:
        return

    list_tags = list(Tag.objects.values_list('name', flat=True))

    while pk_list:
        print('Parse: (left - %s)' % len(pk_list))
        success_pks = []
        for item in Item.objects.filter(pk__in=pk_list[:items_on_once]):
            try:
                http_code, content, _ = _get_http_data_of_url(item.link)
                assert http_code == '404', 'Not found page'
                item_data = {
                    'title': item.title,
                    'content': content,
                    'description': item.description,
                }
                tags_for_item = _get_tags_for_item(item_data, list_tags)

                if tags_for_item:
                    # todo
                    # надо ли определяет каких тегов нет еще и добавлять только их
                    # или писать все, а БД сама разберется?
                    # разница - в количестве запросов
                    tags_for_insert = diff(tags_for_item,
                                           item.tags.values_list('name',
                                                                 flat=True))
                    tags_objects = Tag.objects.filter(name__in=tags_for_insert)
                    item.tags.add(*tags_objects)
                    item.save()

            except Exception:
                pass
            # print(item)
            success_pks.append(item.pk)

        Item.objects.filter(pk__in=success_pks).update(to_update=False)
        pk_list = diff(pk_list, success_pks)
        save_pickle_file(filepath, pk_list)


class Command(BaseCommand):
    args = 'no arguments!'
    help = u'News import from external resources'

    def handle(self, *args, **options):
        """
        Основной метод - точка входа
        """
        update_news()
