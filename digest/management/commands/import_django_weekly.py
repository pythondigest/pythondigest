from collections.abc import Sequence
from typing import Union

import lxml.html as html
from bs4 import BeautifulSoup
from bs4.element import Tag

from django.core.management.base import BaseCommand

from digest.management.commands import save_news_item
from digest.management.commands.import_python_weekly import (
    _apply_rules_wrap,
    _get_content,
)
from digest.models import ITEM_STATUS_CHOICES, ParsingRules, Resource, Section

Parseble = Union[BeautifulSoup, html.HtmlElement]


def _get_blocks(url: str) -> Sequence[BeautifulSoup]:
    """
    Grab all blocks containing news titles and links
    from URL
    """
    result = []
    content = _get_content(url)
    if content:
        try:
            page = html.fromstring(content)
            result = page.find_class("subtitle")
        except OSError:
            page = BeautifulSoup(content, "lxml")
            result = page.findAll("div", {"class": "subtitle"})
    return result


def _get_block_item(block: Parseble) -> dict[str, str | int | Resource]:
    """Extract all data (link, title, description) from block"""
    resource, created = Resource.objects.get_or_create(
        title="Django Weekly", link="http://djangoweekly.com/"
    )

    if isinstance(block, Tag):
        # Handle BeautifulSoup element
        link = block.findAll("a")[0]
        url = link["href"]
        title = link.string
        try:
            bl = block.next_sibling.text
            text = str(bl)
            text = text.replace("<br/>", "").strip()
        except AttributeError:
            return {}
    else:
        # Handle LXML element
        link = block.cssselect("a")[0]
        url = link.attrib["href"]
        title = link.text
        _text = block.getnext()
        if _text is None:
            return {}
        _text = _text.xpath("./text()")
        if _text:
            _text = _text[0]
        else:
            _text = ""

        text = _text.replace("<br/>", "").strip()

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


def main(url):
    data = {
        "query_rules": ParsingRules.objects.filter(is_activated=True).all(),
        "query_sections": Section.objects.all(),
        "query_statuses": [x[0] for x in ITEM_STATUS_CHOICES],
    }
    _apply_rules = _apply_rules_wrap(**data)

    block_items = map(_get_block_item, _get_blocks(url))
    list(map(save_news_item, map(_apply_rules, block_items)))


# Написать тест с использованием ссылки
# http://djangoweekly.com/blog/post/django-weekly-27-advanced-django-querying-django-signals-elasticbeanstalk-and-more


class Command(BaseCommand):
    args = "no arguments!"
    help = ""

    def add_arguments(self, parser):
        parser.add_argument("url", type=str)

    def handle(self, *args, **options):
        if "url" in options:
            main(options["url"])
        else:
            print("Not found folder path")
