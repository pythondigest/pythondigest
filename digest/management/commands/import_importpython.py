# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from urllib.error import URLError
from urllib.request import urlopen

from typing import Sequence, Dict, Union, Tuple

from django.core.management.base import BaseCommand
from bs4 import BeautifulSoup

from digest.models import (
    # ITEM_STATUS_CHOICES,
    # ParsingRules,
    # Section,
    Resource
)

ResourceDict = Dict[str, Union[str, int, Resource]]
ItemTuple = Tuple[BeautifulSoup, BeautifulSoup]


class ImportPythonParser(object):
    BASE_URL = "http://importpython.com"
    RESOURCE_NAME = "importpython"

    def __init__(self):
        pass

    def _get_url_content(self, url: str) -> str:
        """Gets text from URL's response"""
        try:
            result = urlopen(url, timeout=10).read()
        except URLError:
            return ''
        else:
            return result

    def get_latest_issue_number(self):
        """Returns latest issue number"""
        raise NotImplemented

    @classmethod
    def get_issue_url(cls, number: int) -> str:
        """Returns issue URL corresponding to the issue number"""
        number = int(number)
        if number >= 16:
            return "/".join([cls.BASE_URL, "newsletter", "no", str(number)])
        elif 12 <= number <= 15:
            return "/".join([cls.BASE_URL, "newsletter", "draft", str(number)])
        elif 2 <= number <= 14:
            return "/".join([cls.BASE_URL, "static", "files", "issue{}.html".format(str(number))])
        else:
            raise ValueError("Incorre page number: {}".format(number))

    def _get_all_news_blocks(self,
                             soap: BeautifulSoup) -> Sequence[ItemTuple]:
        """Returns sequence of blocks that present single news"""
        subtitle_els = soap.find_all("div", "subtitle")
        body_texts = [el.find_next_sibling("div") for el in subtitle_els]
        return list(zip(subtitle_els, body_texts))

    def _get_block_dict(self,
                        el: Tuple[BeautifulSoup,
                                  BeautifulSoup]) -> ResourceDict:
        # resource = Resource.objects.get(title='ImportPython')

        subtitle, body = el

        title = subtitle.find("a").text
        url = subtitle.find("a")['href']
        text = body.text
        resource = ""
        return {
            'title': title,
            'link': url,
            'raw_content': text,
            'http_code': 200,
            'content': text,
            'description': text,
            'resource': resource,
            'language': 'en',
        }

    def get_blocks(self, url: str) -> Sequence[ResourceDict]:
        """Get news dictionaries from the specified URL"""
        content = self._get_url_content(url)
        soup = BeautifulSoup(content, "lxml")
        blocks = self._get_all_news_blocks(soup)
        items = map(self._get_block_dict, blocks)
        return list(items)


def main(url: str="", number: int="") -> None:
    parser = ImportPythonParser()
    if number and not url:
        url = parser.get_issue_url(int(number))
    blocks = parser.get_blocks(url)


class Command(BaseCommand):
    args = 'no arguments!'
    help = """This command parses importpython.com site\
 and saves posts from it to the database"""

    def add_arguments(self, parser):
        parser.add_argument('--url', type=str, help='Url to parse data from')
        parser.add_argument('--number',
                            type=int,
                            help='Number of "issue" to parse')

    def handle(self, *args, **options):
        if 'url' in options and options['url'] is not None:
            main(url=options['url'])
        elif 'number' in options and options['number'] is not None:
            main(number=options['number'])
        else:
            print('No URL or Issue number for parser found')
