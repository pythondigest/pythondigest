from unittest.mock import patch

from django.test import TestCase

from digest.management.commands import get_tweets_by_url
from digest.management.commands.import_news import _parse_tweets_data
from digest.models import AutoImportResource
from digest.utils import MockResponse, read_fixture


class ImportTweetsTest(TestCase):
    def setUp(self):
        self.res_twitter = AutoImportResource.objects.create(
            title="Test",
            link="https://twitter.com/pythontrending",
            type_res="twitter",
            excl="http://consumerfinance.gov",
            incl="framework",
        )

    def test_get_tweets(self):
        test_name = "fixture_test_import_news_test_get_tweets.txt"
        self.patcher = patch("digest.management.commands.urlopen")
        self.urlopen_mock = self.patcher.start()
        self.urlopen_mock.return_value = MockResponse(read_fixture(test_name))

        tweets = get_tweets_by_url(self.res_twitter.link)

        self.patcher.stop()
        self.assertEqual(len(tweets), 19)

        for x in tweets:
            self.assertEqual(len(x), 3)
            self.assertEqual(x[2], 200)
            self.assertEqual("http" in x[1], True)

        return tweets

    def test_exclude(self):
        dsp = _parse_tweets_data(self.test_get_tweets(), self.res_twitter)
        self.assertEqual(len(dsp), 3)
