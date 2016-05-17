# -*- encoding: utf-8 -*-
import datetime
from functools import partial

from django.test import TestCase
from mock import patch

from digest.management.commands.import_news import get_items_from_rss, \
    _is_old_rss_news, is_not_exists_rss_item
from digest.models import AutoImportResource, Item, Section
from digest.utils import MockResponse
from digest.utils import read_fixture


class ImportRSSTest(TestCase):
    def setUp(self):
        self.res_rss = AutoImportResource.objects.create(title='Test2',
                                                         link='http://planetpython.org/rss20.xml',
                                                         type_res='rss')

        self.section = Section(title='Статьи')
        self.section.save()
        test_name = 'fixture_test_import_news_test_rss.txt'

        self.patcher = patch('digest.management.commands.urlopen')
        self.urlopen_mock = self.patcher.start()
        self.urlopen_mock.return_value = MockResponse(read_fixture(test_name))

    def tearDown(self):
        self.patcher.stop()

    def test_get_rss_items(self):
        rss_items = get_items_from_rss(self.res_rss.link)
        self.assertEqual(len(rss_items), 25)

    def test_filter_old_news_rss(self):
        rss_items = get_items_from_rss(self.res_rss.link)
        old_data = datetime.date(2005, 7, 14)
        rss_items[0]['related_to_date'] = old_data
        rss_items[4]['related_to_date'] = old_data
        rss_items[8]['related_to_date'] = old_data
        rss_items[12]['related_to_date'] = old_data

        self.assertEqual(len(list(filter(_is_old_rss_news, rss_items))), 21)

    def test_filter_exists_news(self):
        rss_items = get_items_from_rss(self.res_rss.link)

        Item(title=rss_items[0]['title'], link=rss_items[0]['link'],
             section=self.section).save()
        Item(title=rss_items[1]['title'], link=rss_items[1]['link'],
             section=self.section).save()
        Item(title=rss_items[2]['title'], link=rss_items[2]['link'],
             section=self.section).save()
        Item(title=rss_items[3]['title'], link=rss_items[3]['link'],
             section=self.section).save()
        Item(title=rss_items[4]['title'], link=rss_items[4]['link'],
             related_to_date=datetime.date(2005, 7, 14),
             section=self.section).save()
        Item(title=rss_items[5]['title'], link=rss_items[5]['link'],
             related_to_date=datetime.date(2016, 4, 12),
             section=self.section).save()

        fil = partial(is_not_exists_rss_item,
                      minimum_date=datetime.date(2016, 4, 11))
        self.assertEqual(len(list(filter(fil, rss_items))), 20)
