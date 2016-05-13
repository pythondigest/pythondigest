from mock import patch

from django.test import TestCase

from digest.management.commands.import_importpython import ImportPythonParser


class ImportPythonWeeklyTest(TestCase):

    def test_correctly_creates_issue_urls(self):
        self.assertEqual(ImportPythonParser.get_issue_url(2),
                         "http://importpython.com/static/files/issue2.html")
        self.assertEqual(ImportPythonParser.get_issue_url(12),
                         "http://importpython.com/newsletter/draft/12")
        self.assertEqual(ImportPythonParser.get_issue_url(56),
                         "http://importpython.com/newsletter/no/56")
        with self.assertRaises(ValueError):
            ImportPythonParser.get_issue_url(-100)
