"""Script for import package releases from pypi site.
A lot of hindi code"""

import datetime
import logging
from time import mktime

import feedparser
from django.core.management.base import BaseCommand

from digest.management.commands import save_news_item
from digest.models import Issue, Item, Package, Resource, Section, get_start_end_of_week

logger = logging.getLogger(__name__)


def _generate_release_item(
    package_version: str,
    link: str,
    resource: Resource,
    section: Section,
    package: Package,
):
    name = f"{package.name} - {package_version}"
    description = '{0}. Скачать можно по ссылке: <a href="{1}">{1}</a>'.format(
        package.description,
        package.link.replace("http", "https"),
    )
    return {
        "title": name,
        "link": link,
        "resource": resource,
        "status": "active",
        "section": section,
        "language": "en",
        "description": description,
    }


def off_other_release_news(news, package: Package):
    news.filter(
        title__startswith=package.name,
        description__contains=package.link,
    ).update(status="moderated")


def check_previous_news_of_package(news, package: Package):
    items = news.filter(
        title__startswith=package.name,
        description__contains=package.link,
    )
    assert items.count() <= 1, "Many items for library"
    return items.count() != 0


def parse_rss(package: Package):
    package_rss_releases = package.link_rss

    today = datetime.date.today()
    week_before = today - datetime.timedelta(weeks=1)
    try:
        _start_week, _end_week = get_start_end_of_week(today)
        _ = Issue.objects.filter(date_from=_start_week, date_to=_end_week)

        assert _.count() <= 1, "Many ISSUE on week"
        _ = None if _.count() == 0 else _[0]
        news = Item.objects.filter(issue=_, status="active") if _ is not None else []

        section = Section.objects.get(title="Релизы")
        resource = Resource.objects.get(title="PyPI")
    except Exception as e:
        print(e)
        return

    for n in feedparser.parse(package_rss_releases).entries:
        package_version = n.title
        # skip non stable versions
        if "b" in package_version or "a" in package_version or "rc" in package_version:
            continue

        if Item.objects.filter(link=n.link).exists():
            continue

        time_struct = getattr(n, "published_parsed", None)
        if time_struct:
            _timestamp = mktime(time_struct)
            dt = datetime.datetime.fromtimestamp(_timestamp)
            if dt.date() < week_before:
                continue

        try:
            if news and check_previous_news_of_package(news, package):
                off_other_release_news(news, package)

            item_data = _generate_release_item(package_version, n.link, resource, section, package)
            save_news_item(item_data)
            print(f"> Save news for version - {package_version}")
        except Exception as e:
            print(e)
            continue


def parse_release_rss():
    queryset = Package.objects.filter(is_active=True)
    for package in queryset:
        print(f"Processing...{package.name}")
        parse_rss(package)
        # break


class Command(BaseCommand):
    args = "no arguments!"
    help = "News import from external resources"

    def handle(self, *args, **options):
        parse_release_rss()
