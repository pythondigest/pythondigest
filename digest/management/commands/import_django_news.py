"""
python manage.py import_django_news URL

example:
python manage.py import_django_news 'https://django-news.com/issues/160'
"""

import logging
from collections.abc import Sequence

import lxml.html as html
from django.core.management.base import BaseCommand
from lxml import etree
from sentry_sdk import capture_exception

from digest.management.commands import ignore_url, make_get_request, save_news_item
from digest.management.commands.import_python_weekly import _apply_rules_wrap
from digest.models import ITEM_STATUS_CHOICES, ParsingRules, Resource, Section

logger = logging.getLogger(__name__)


def _get_blocks(url: str, root_class, css_class) -> Sequence[html.HtmlElement]:
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
        result = page.find_class(root_class)[0]
        result = result.cssselect(css_class)
    return result


def _get_block_item(block: html.HtmlElement) -> dict[str, str | int | Resource]:
    """Extract all data (link, title, description) from block"""

    # extract link info
    link = block.cssselect("span.item__footer-link")[0].cssselect("a")[0]
    url = link.attrib["href"]
    title = block.cssselect("h3.item__title")[0].text_content().replace("\n", "").strip()
    description = block.cssselect("p")
    if description:
        text = description[0].text_content().replace("\n", "").strip()
    else:
        text = ""

    if url.startswith("https://cur.at"):
        # Resolve original url
        try:
            response = make_get_request(url)
            url = response.url
        except Exception as e:
            capture_exception(e)

    return {
        "title": title,
        "link": url,
        "raw_content": text,
        "http_code": 200,
        "content": text,
        "description": text,
        "language": "en",
    }


def main(url):
    data = {
        "query_rules": ParsingRules.objects.filter(is_activated=True).all(),
        "query_sections": Section.objects.all(),
        "query_statuses": [x[0] for x in ITEM_STATUS_CHOICES],
    }
    _apply_rules = _apply_rules_wrap(**data)

    resource, _ = Resource.objects.get_or_create(title="Django News", link="https://django-news.com/")

    # items
    blocks = _get_blocks(url, "issue__body", "div.item--link")

    for block in blocks:
        # print(etree.tostring(block))
        block_item = _get_block_item(block)
        if not block_item:
            continue

        if ignore_url(block_item["link"]):
            continue

        # break
        block_item["resource"] = resource
        _apply_rules(block_item)
        save_news_item(block_item)


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
