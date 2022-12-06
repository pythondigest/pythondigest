from unittest.mock import Mock, patch

from django.test import TestCase

from digest.management.commands import make_get_request
from digest.management.commands.import_python_weekly import _get_blocks
from digest.utils import MockResponse, read_fixture


class ImportPythonWeeklyBadTest(TestCase):
    def test_get_content_bad_link(self):
        response = make_get_request("htt://googl.fa")
        self.assertEqual(response, None)


class ImportPythonWeeklyTest(TestCase):
    def setUp(self):
        self.url = "http://us2.campaign-archive1.com/?u=e2e180baf855ac797ef407fc7&id=31658452eb&utm_content=buffera9dc3&utm_medium=social&utm_source=twitter.com&utm_campaign=buffer"

        test_name = "fixture_test_import_python_weekly_test_get_blocks.txt"

        self.patcher = patch("requests.get")
        requests_mock = self.patcher.start()
        response = MockResponse(read_fixture(test_name))
        response.status_code = 200
        response.raise_for_status = Mock()
        requests_mock.return_value = response

    def tearDown(self):
        self.patcher.stop()

    def test_get_content(self):
        response = make_get_request(self.url)
        content = response.text
        self.assertEqual(len(content), 47764)

    def test_get_blocks(self):
        blocks = _get_blocks(self.url)
        self.assertEqual(len(blocks), 28)
        return blocks
