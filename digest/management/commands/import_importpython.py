"""
This module contains command to obtain news from importpython.com
and save the to database.
To use it run something like
python manage.py import_importpython --number 67
If no args specified parses latest news page.
"""

from typing import Union
from urllib.error import URLError
from urllib.request import urlopen

from bs4 import BeautifulSoup

from django.core.management.base import BaseCommand

from digest.management.commands import (
    apply_parsing_rules,
    apply_video_rules,
    save_news_item,
)
from digest.models import ITEM_STATUS_CHOICES, ParsingRules, Resource, Section

ResourceDict = dict[str, Union[str, int, Resource]]
ItemTuple = tuple[BeautifulSoup, BeautifulSoup]


class ImportPythonParser:
    BASE_URL = "http://importpython.com"
    RESOURCE_NAME = "importpython"

    def __init__(self):
        pass

    @staticmethod
    def _get_url_content(url: str) -> str:
        """Gets text from URL's response"""
        try:
            result = urlopen(url, timeout=10).read()
        except URLError:
            return ""
        else:
            return result

    @classmethod
    def get_latest_issue_url(cls) -> str:
        """Returns latest issue URL"""
        archive_url = "/".join([cls.BASE_URL, "newsletter", "archive"])
        content = cls._get_url_content(archive_url)
        soup = BeautifulSoup(content, "lxml")
        el = soup.find_all("div", "info")[0]
        href = el.find("h2").find("a")["href"]
        link = cls.BASE_URL + href
        return link

    @classmethod
    def get_issue_url(cls, number: int) -> str:
        """Returns issue URL corresponding to the issue number"""
        number = int(number)
        if number >= 16:
            return "/".join([cls.BASE_URL, "newsletter", "no", str(number)])
        elif 12 <= number <= 15:
            return "/".join([cls.BASE_URL, "newsletter", "draft", str(number)])
        elif 2 <= number <= 14:
            return "/".join(
                [cls.BASE_URL, "static", "files", f"issue{str(number)}.html"]
            )
        else:
            raise ValueError(f"Incorre page number: {number}")

    def _get_all_news_blocks(self, soap: BeautifulSoup) -> list[ItemTuple]:
        """Returns sequence of blocks that present single news"""
        # TODO: add tags parsing
        subtitle_els = soap.find_all("div", "subtitle")
        body_texts = [el.find_next_sibling("div") for el in subtitle_els]
        return list(zip(subtitle_els, body_texts))

    def _get_block_dict(self, el: tuple[BeautifulSoup, BeautifulSoup]) -> ResourceDict:
        resource, created = Resource.objects.get_or_create(
            title="ImportPython", link="http://importpython.com"
        )

        subtitle, body = el
        title = subtitle.find("a").text
        url = subtitle.find("a")["href"]
        text = body.text
        return {
            "title": title,
            "link": url,
            "raw_content": text,
            "http_code": 200,
            "content": text,
            "description": text,
            "resource": resource,
            "language": "en",
        }

    def get_blocks(self, url: str) -> list[ResourceDict]:
        """Get news dictionaries from the specified URL"""
        content = self._get_url_content(url)
        soup = BeautifulSoup(content, "lxml")
        blocks = self._get_all_news_blocks(soup)
        items = map(self._get_block_dict, blocks)
        return list(items)


def _apply_rules_wrap(**kwargs):
    # TODO: move this function into separate module
    # as it is used in several parsing modules
    rules = kwargs

    def _apply_rules(item: dict) -> dict:
        item.update(
            apply_parsing_rules(item, **rules) if kwargs.get("query_rules") else {}
        )
        item.update(apply_video_rules(item))
        return item

    return _apply_rules


def main(url: str = "", number: int = "") -> None:
    data = {
        "query_rules": ParsingRules.objects.filter(is_activated=True).all(),
        "query_sections": Section.objects.all(),
        "query_statuses": [x[0] for x in ITEM_STATUS_CHOICES],
    }
    _apply_rules = _apply_rules_wrap(**data)

    parser = ImportPythonParser()
    if number and not url:
        url = parser.get_issue_url(number)
    if not number and not url:
        url = parser.get_latest_issue_url()
    blocks = parser.get_blocks(url)
    with_rules_applied = map(_apply_rules, blocks)
    for block in with_rules_applied:
        save_news_item(block)


class Command(BaseCommand):
    help = """This command parses importpython.com site\
 and saves posts from it to the database.
 You may either specify url by using --url argument, or
 implicitly specify issue number by using --number argument."""

    def add_arguments(self, parser):
        parser.add_argument("--url", type=str, help="Url to parse data from")
        parser.add_argument("--number", type=int, help='Number of "issue" to parse')

    def handle(self, *args, **options):
        if "url" in options and options["url"] is not None:
            main(url=options["url"])
        elif "number" in options and options["number"] is not None:
            main(number=int(options["number"]))
        else:
            main()
