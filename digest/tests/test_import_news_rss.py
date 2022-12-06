import datetime
from unittest.mock import Mock, patch

from django.test import TestCase

from digest.management.commands.import_news import get_items_from_rss, is_skip_news
from digest.models import AutoImportResource, Item, Section
from digest.utils import MockResponse, read_fixture


class ImportRSSTest(TestCase):
    def setUp(self):
        test_name = "fixture_test_import_news_test_rss.txt"

        self.patcher = patch("requests.get")
        requests_mock = self.patcher.start()
        response = MockResponse(read_fixture(test_name))
        response.status_code = 200
        response.raise_for_status = Mock()
        requests_mock.return_value = response

        self.res_rss = AutoImportResource.objects.create(
            title="Test2", link="https://planetpython.org/rss20.xml", type_res="rss"
        )

        self.section = Section(title="Статьи")
        self.section.save()

    def tearDown(self):
        self.patcher.stop()

    def test_get_rss_items(self):
        rss_items = get_items_from_rss(self.res_rss.link)

        self.assertEqual(len(rss_items), 25)

    def test_filter_old_news_rss(self):
        rss_items = get_items_from_rss(self.res_rss.link)

        old_data = datetime.date(2005, 7, 14)
        rss_items[0]["related_to_date"] = old_data
        rss_items[4]["related_to_date"] = old_data
        rss_items[8]["related_to_date"] = old_data
        rss_items[12]["related_to_date"] = old_data

        actual_items = [
            x
            for x in rss_items
            if not is_skip_news(
                x,
                minimum_date=old_data + datetime.timedelta(days=1),
            )
        ]
        self.assertEqual(len(actual_items), 21)

    def test_filter_exists_news(self):
        rss_items = get_items_from_rss(self.res_rss.link)

        Item(
            title=rss_items[0]["title"], link=rss_items[0]["link"], section=self.section
        ).save()
        Item(
            title=rss_items[1]["title"], link=rss_items[1]["link"], section=self.section
        ).save()
        Item(
            title=rss_items[2]["title"], link=rss_items[2]["link"], section=self.section
        ).save()
        Item(
            title=rss_items[3]["title"], link=rss_items[3]["link"], section=self.section
        ).save()

        actual_items = [
            x
            for x in rss_items
            if not is_skip_news(
                x,
                minimum_date=datetime.date(2000, 4, 11),
            )
        ]
        self.assertEqual(len(actual_items), 21)
