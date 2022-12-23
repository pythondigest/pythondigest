"""
python manage.py import_awesome_python_weekly URL

example:
python manage.py import_awesome_python_weekly 'https://python.libhunt.com/newsletter/343'
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
    link = block.cssselect("a.title")[0]
    url = link.attrib["href"]
    title = link.text_content().replace("\n", "").strip()

    description = block.cssselect("p.description")
    if description:
        text = description[0].text_content().replace("\n", "").strip()
    else:
        text = ""

    if "libhunt.com/r/" in url:
        # Resolve original url for package
        try:
            response = make_get_request(url)
            url = response.url
            content = response.text
            page = html.fromstring(content)
            boxed_links = page.find_class("boxed-links")[0]
            link = boxed_links.xpath("//a[text()='Source Code']")[0]
            url = link.get("href")
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

    resource, _ = Resource.objects.get_or_create(title="Awesome Python", link="https://python.libhunt.com/")

    block_domains = [
        "www.meetup.com",
        "medium.com",
        "medium.",
        "thisweekin.io",
        "google.com",
        "apple.com",
        "tinyurl.com",
        "python.libhunt.com",
    ]

    # news
    blocks = _get_blocks(url, "newsletter-stories", "a.title")
    # projects
    blocks.extend(_get_blocks(url, "newsletter-projects", "li.project"))

    for block in blocks:
        link = block.cssselect("a.title")[0].attrib["href"]
        logger.info(f"Work with url - {link}")
        if any([x in link for x in block_domains]):
            continue

        if link == "https://python.libhunt.com/":
            continue

        block_item = _get_block_item(block)
        if not block_item:
            continue

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
