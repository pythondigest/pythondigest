# -*- encoding: utf-8 -*-
import os

from django.test import TestCase
from mock import patch

from digest.management.commands import get_tweets_by_url
from digest.models import AutoImportResource


def save_fixture(name, data, mode='wb'):
    with open(os.path.join(os.path.dirname(__file__), name), mode) as fio:
        fio.write(data)


def read_fixture(name, mode='rb'):
    with open(os.path.join(os.path.dirname(__file__), name), mode) as fio:
        return fio.read()


class MockResponse(object):
    def __init__(self, resp_data, code=200, msg='OK'):
        self.resp_data = resp_data
        self.code = code
        self.msg = msg
        self.headers = {'content-type': 'text/plain; charset=utf-8'}

    def read(self):
        return self.resp_data

    def getcode(self):
        return self.code


class ImportTweetsTest(TestCase):
    def setUp(self):
        self.res_twitter = AutoImportResource.objects.create(name='Test',
                                                             link='https://twitter.com/pythontrending',
                                                             type_res='twitter')
        self.res_rss = AutoImportResource.objects.create(name='Test2',
                                                         link='http://planetpython.org/rss20.xml',
                                                         type_res='rss')

    def test_get_tweets(self):
        test_name = 'fixture_test_import_news_test_get_tweets.txt'

        self.patcher = patch('urllib.request.urlopen')
        self.urlopen_mock = self.patcher.start()
        self.urlopen_mock.return_value = MockResponse(read_fixture(test_name))

        tweets = get_tweets_by_url(self.res_twitter.link)
        self.patcher.stop()

        self.assertEqual(len(tweets), 19)

        for x in tweets:
            self.assertEqual(len(x), 3)
            self.assertEqual(x[2], 200)
            self.assertEqual('http' in x[1], True)
