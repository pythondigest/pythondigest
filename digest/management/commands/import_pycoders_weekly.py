"""
python manage.py import_python_weekly URL

example:
python manage.py import_pycoders_weekly 'https://pycoders.com/issues/556'
"""

import logging
from collections.abc import Sequence

import lxml.html as html
from django.core.management.base import BaseCommand
from sentry_sdk import capture_exception

from digest.management.commands import make_get_request, save_news_item
from digest.management.commands.import_python_weekly import _apply_rules_wrap
from digest.models import ITEM_STATUS_CHOICES, ParsingRules, Resource, Section

logger = logging.getLogger(__name__)


def _get_blocks(url: str) -> Sequence[html.HtmlElement]:
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
        result = page.xpath("//td[@id = 'bodyCell']")[0]
        result = result.cssselect("span")
    return result


def _get_block_item(block: html.HtmlElement) -> dict[str, str | int | Resource]:
    """Extract all data (link, title, description) from block"""

    if "#AAAAAA" in block.attrib["style"]:
        return

    # print(etree.tostring(block))

    # extract link info
    link = block.cssselect("a")[0]
    url = link.attrib["href"]
    title = link.text_content()

    if url.startswith("https://pycoders.com/link/"):
        # Resolve original url
        try:
            response = make_get_request(url)
            url = response.url
        except Exception as e:
            capture_exception(e)

    # extract description info
    # getnext().getnext() because description info is not inner block
    try:
        description_block = block.getnext().getnext()
    except AttributeError:
        text = ""
    else:
        text = description_block.text_content()
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


def main(url):
    data = {
        "query_rules": ParsingRules.objects.filter(is_activated=True).all(),
        "query_sections": Section.objects.all(),
        "query_statuses": [x[0] for x in ITEM_STATUS_CHOICES],
    }
    _apply_rules = _apply_rules_wrap(**data)

    resource, _ = Resource.objects.get_or_create(title="PyCoders", link="https://pycoders.com")

    block_domains = [
        "www.meetup.com",
        "medium.com",
        "medium.",
        "thisweekin.io",
        "google.com",
        "apple.com",
        "tinyurl.com",
        "pycoders.com/issues/",
        "realpython.com/account/join-team/",
        "realpython.com/office-hours/",
    ]
    for block in _get_blocks(url):
        if not block.cssselect("a"):
            continue

        link = block.cssselect("a")[0].attrib["href"]
        logger.info(f"Work with url - {link}")

        if link == "https://pycoders.com":
            continue

        block_item = _get_block_item(block)
        if not block_item:
            continue

        link = block_item["link"]
        if any([x in link for x in block_domains]):
            continue

        block_item["resource"] = resource
        # pprint.pprint(block_item)

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
