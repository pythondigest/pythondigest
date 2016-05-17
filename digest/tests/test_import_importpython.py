from django.test import TestCase
from mock import patch

from digest.management.commands.import_importpython import ImportPythonParser
from digest.utils import MockResponse, read_fixture


class ImportPythonWeeklyTest(TestCase):
    def setUp(self):
        self.url = "http://importpython.com/newsletter/no/60/"

        test_fixture = 'fixture_test_import_importpython_test_get_blocks.txt'
        self.patcher = patch(
            'digest.management.commands.import_importpython.urlopen')
        self.urlopen_mock = self.patcher.start()
        self.urlopen_mock.return_value = MockResponse(
            read_fixture(test_fixture))
        self.parser = ImportPythonParser()

    def tearDown(self):
        self.patcher.stop()

    def test_correctly_creates_issue_urls(self):
        self.assertEqual(ImportPythonParser.get_issue_url(2),
                         "http://importpython.com/static/files/issue2.html")
        self.assertEqual(ImportPythonParser.get_issue_url(12),
                         "http://importpython.com/newsletter/draft/12")
        self.assertEqual(ImportPythonParser.get_issue_url(56),
                         "http://importpython.com/newsletter/no/56")
        with self.assertRaises(ValueError):
            ImportPythonParser.get_issue_url(-100)

    def test_correct_number_of_blocks_parsed(self):
        blocks = self.parser.get_blocks(self.url)
        self.assertEqual(len(blocks), 25)

    def test_correctly_parses_block(self):
        blocks = self.parser.get_blocks(self.url)
        block = blocks[0]
        self.assertEqual(block['link'],
                         "https://talkpython.fm/episodes/show/44/project-jupyter-and-ipython")
        self.assertEqual(block['title'],
                         "Project Jupyter and IPython Podcast Interview")
        self.assertEqual(block['content'],
                         "One of the fastest growing areas in Python is scientific computing. In scientific computing with Python, there are a few key packages that make it special. These include NumPy / SciPy / and related packages. The one that brings it all together, visually, is IPython (now known as Project Jupyter). That's the topic on episode 44 of Talk Python To Me. ")

    def test_correctly_gets_latest_url(self):
        test_latest = 'fixture_test_import_importpython_test_get_latest_url.txt'
        self._old_return_value = self.urlopen_mock.return_value
        self.urlopen_mock.return_value = MockResponse(read_fixture(test_latest))
        latest_url = self.parser.get_latest_issue_url()
        self.assertEqual(latest_url,
                         "http://importpython.com/newsletter/no/72/")
