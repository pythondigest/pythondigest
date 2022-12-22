"""
python manage.py import_python_weekly URL

example:
python manage.py import_python_weekly 'https://python.thisweekin.io/python-weekly-issue-57-6773a17532df?source=rss----26a6525a27bc---4'
"""
from collections.abc import Sequence
from typing import Union

import lxml.html as html
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand

from digest.management.commands import apply_parsing_rules, apply_video_rules, make_get_request, save_news_item
from digest.models import ITEM_STATUS_CHOICES, ParsingRules, Resource, Section

Parseble = Union[BeautifulSoup, html.HtmlElement]


def _get_blocks(url: str) -> Sequence[BeautifulSoup]:
    """
    Grab all blocks containing news titles and links
    from URL
    """
    result = []
    response = make_get_request(url)
    if not response:
        return result

    content = response.text
    if content:
        page = html.fromstring(content)
        result = page.find_class("meteredContent")[0]
        result = result.cssselect("a")
    return result


def _get_block_item(block: Parseble) -> dict[str, str | int | Resource]:
    """Extract all data (link, title, description) from block"""

    link = block.cssselect("a")[0]
    url = link.attrib["href"]
    title = block.cssselect("h2")[0].text_content()
    text = block.cssselect("h3")[0].text_content()

    text = text.replace("<br/>", "").strip()

    return {
        "title": title,
        "link": url,
        "raw_content": text,
        "http_code": 200,
        "content": text,
        "description": text,
        "language": "en",
    }


def _apply_rules_wrap(**kwargs):
    rules = kwargs

    def _apply_rules(item: dict) -> dict:
        item.update(apply_parsing_rules(item, **rules) if kwargs.get("query_rules") else {})
        item.update(apply_video_rules(item))
        return item

    return _apply_rules


def main(url):
    data = {
        "query_rules": ParsingRules.objects.filter(is_activated=True).all(),
        "query_sections": Section.objects.all(),
        "query_statuses": [x[0] for x in ITEM_STATUS_CHOICES],
    }
    _apply_rules = _apply_rules_wrap(**data)

    resource, _ = Resource.objects.get_or_create(title="PythonWeekly", link="http://www.pythonweekly.com/")

    block_domains = [
        "medium.com",
        "medium.",
        "thisweekin.io",
        "google.com",
        "apple.com",
        "tinyurl.com",
    ]
    rel_list = [
        "noopener",
        "follow",
        "ugc",
    ]
    for block in _get_blocks(url):
        if any([x in block.get("href") for x in block_domains]):
            continue

        rel = block.get("rel")
        if any([x not in rel for x in rel_list]):
            continue

        block_item = _get_block_item(block)
        block_item["resource"] = resource
        _apply_rules(block_item)

        save_news_item(block_item)


# Написать тест с использованием ссылки
# http://us2.campaign-archive.com/?u=e2e180baf855ac797ef407fc7&id=d4b2a101de
# http://us2.campaign-archive.com/?u=e2e180baf855ac797ef407fc7&id=0a5d4ce3e5
# http://us2.campaign-archive.com/?u=e2e180baf855ac797ef407fc7&id=a68acae6d6


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
