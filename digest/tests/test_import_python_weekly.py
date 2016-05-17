# -*- encoding: utf-8 -*-


from django.test import TestCase
from mock import patch

from digest.management.commands.import_python_weekly import _get_content, \
    _get_blocks
from digest.utils import MockResponse
from digest.utils import read_fixture


class ImportPythonWeeklyBadTest(TestCase):
    def test_get_content_bad_link(self):
        content = _get_content('htt://googl.fa')
        self.assertEqual(content, '')


class ImportPythonWeeklyTest(TestCase):
    def setUp(self):
        self.url = 'http://us2.campaign-archive1.com/?u=e2e180baf855ac797ef407fc7&id=31658452eb&utm_content=buffera9dc3&utm_medium=social&utm_source=twitter.com&utm_campaign=buffer'

        test_name = 'fixture_test_import_python_weekly_test_get_blocks.txt'
        self.patcher = patch(
            'digest.management.commands.import_python_weekly.urlopen')
        self.urlopen_mock = self.patcher.start()
        self.urlopen_mock.return_value = MockResponse(read_fixture(test_name))

        # list(map(save_item, map(_apply_rules, map(_get_block_item, _get_blocks(url)))))

    def tearDown(self):
        self.patcher.stop()

    def test_get_content(self):
        content = _get_content(self.url)
        self.assertEqual(len(content), 48233)

    def test_get_blocks(self):
        blocks = _get_blocks(self.url)
        self.assertEqual(len(blocks), 28)
        return blocks
