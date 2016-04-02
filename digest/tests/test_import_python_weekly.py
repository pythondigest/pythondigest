# -*- encoding: utf-8 -*-


url = 'http://us2.campaign-archive1.com/?u=e2e180baf855ac797ef407fc7&id=31658452eb&utm_content=buffera9dc3&utm_medium=social&utm_source=twitter.com&utm_campaign=buffer'

# -*- encoding: utf-8 -*-

from django.test import TestCase
from mock import patch

from digest.management.commands import get_tweets_by_url
from digest.utils import MockResponse
from digest.utils import read_fixture


class ImportPythonWeeklyTest(TestCase):
    def test_get_blocks(self):
        pass
        # test_name = 'fixture_test_import_news_test_get_tweets.txt'
        #
        # self.patcher = patch('urllib.request.urlopen')
        # self.urlopen_mock = self.patcher.start()
        # self.urlopen_mock.return_value = MockResponse(read_fixture(test_name))
        #
        # tweets = get_tweets_by_url(self.res_twitter.link)
        # self.patcher.stop()
        #
        # self.assertEqual(len(tweets), 19)
        #
        # for x in tweets:
        #     self.assertEqual(len(x), 3)
        #     self.assertEqual(x[2], 200)
        #     self.assertEqual('http' in x[1], True)
        # return tweets
