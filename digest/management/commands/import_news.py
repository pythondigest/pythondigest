import datetime
import logging
import re
import socket
from time import mktime
from urllib.error import URLError

import feedparser
import requests
from cache_memoize import cache_memoize
from django.core.management.base import BaseCommand
from requests import TooManyRedirects

from digest.management.commands import (
    apply_parsing_rules,
    apply_video_rules,
    get_readable_content,
    get_tweets_by_url,
    is_weekly_digest,
    make_get_request,
    parse_weekly_digest,
    save_news_item,
)
from digest.models import ITEM_STATUS_CHOICES, AutoImportResource, Item, ParsingRules, Section

logger = logging.getLogger(__name__)


def _parse_tweets_data(data: list, src: AutoImportResource) -> list:
    result = []
    excl = [s.strip() for s in (src.excl or "").split(",") if s]
    for text, link, http_code in data:

        try:
            excl_link = bool([i for i in excl if i in link])
        except TypeError as e:
            print(f"WARNING: (import_news): {e}")
            excl_link = False
        if not excl_link and src.incl in text:
            tw_txt = text.replace(src.incl, "")
            result.append([tw_txt, link, src.resource, http_code])
    return result


def get_tweets():
    result = []
    news_sources = AutoImportResource.objects.filter(type_res="twitter").exclude(in_edit=True).exclude(is_active=False)
    for source in news_sources:
        print("Process twitter", source)
        try:
            result.extend(_parse_tweets_data(get_tweets_by_url(source.link), source))
        except Exception as e:
            print(e)
    return result


def import_tweets(**kwargs):
    logger.info("Import news from Twitter feeds")
    apply_rules = kwargs.get("apply_rules")
    for i in get_tweets():
        try:
            # это помогает не парсить лишний раз ссылку, которая есть
            if Item.objects.filter(link=i[1]).exists():
                continue

            # title = '[!] %s' % i[0] if fresh_google_check(i[1]) else i[0]
            title = i[0]
            item_data = {
                "title": title,
                "link": i[1],
                "http_code": i[3],
                "resource": i[2],
            }
            if is_weekly_digest(item_data):
                parse_weekly_digest(item_data)
            else:
                if apply_rules:
                    data = apply_parsing_rules(item_data, **kwargs) if kwargs.get("query_rules") else {}
                    item_data.update(data)
            save_news_item(item_data)
        except (URLError, TooManyRedirects, socket.timeout) as e:
            print(i, str(e))


@cache_memoize(300)
def get_items_from_rss(rss_link: str, timeout=10) -> list[dict]:
    """
    Get rss content from rss source.

    Function create request to rss source, parse RSS and create list of dict with rss data
    (link, title, description and news data)
    :param rss_link: string, rss link
    :return: list of dicts, each dict includes link, title, description and news data of rss item
    """
    logger.info(f"Get items from rss: {rss_link}")
    rss_items = []
    try:
        response = make_get_request(rss_link)
        if not response:
            return rss_items
        res_news = feedparser.parse(response.content)

        for n in res_news.entries:

            news_time = getattr(n, "published_parsed", None)
            if news_time is not None:
                _timestamp = mktime(news_time)
                news_date = datetime.datetime.fromtimestamp(_timestamp).date()
            else:
                news_date = datetime.date.today()

            # create data dict
            try:
                summary = re.sub("<.*?>", "", n.summary)
            except (AttributeError, KeyError):
                summary = ""

            rss_items.append(
                {
                    "title": n.title,
                    "link": n.link,
                    "description": summary,
                    "related_to_date": news_date,
                }
            )
    except Exception as e:
        print("Exception -> ", str(e))
        rss_items = []

    return rss_items


def is_skip_news(rss_item: dict, minimum_date=None) -> bool:
    """Фильтруем старые новости, а также дубли свежих новостей"""
    if minimum_date is None:
        minimum_date = datetime.date.today() - datetime.timedelta(weeks=1)

    # skip old news by rss date
    if rss_item["related_to_date"] < minimum_date:
        return True

    # skip old duplicated news
    if Item.objects.filter(link=rss_item["link"], related_to_date__gte=minimum_date).exists():
        return True

    return False


def get_data_for_rss_item(rss_item: dict) -> dict:
    if rss_item["link"].startswith("https://twitter.com") and rss_item.get("description"):
        raw_content = rss_item["description"]
        http_code = str(200)
    else:
        response = make_get_request(rss_item["link"])
        if not response:
            return rss_item

        raw_content = response.content.decode()
        http_code = str(200)

    rss_item.update(
        {
            "raw_content": raw_content,
            "http_code": http_code,
            "content": get_readable_content(raw_content),
        }
    )
    return rss_item


def import_rss(**kwargs):
    logger.info("Import news from RSS feeds")
    news_sources = (
        AutoImportResource.objects.filter(type_res="rss").exclude(in_edit=True).exclude(is_active=False).order_by("?")
    )

    apply_rules = kwargs.get("apply_rules")
    logger.info(f"Apply rules: {apply_rules}")

    for source in news_sources:
        logger.info(f"Process RSS {source.title} from {source.link}")
        try:
            logger.info("Extact items from feed")
            news_items = get_items_from_rss(source.link)
            logger.info(f"> Found {len(news_items)} raw items")

            logger.info("Skip old news")
            news_items = [x for x in news_items if not is_skip_news(x)]

            if apply_rules:
                logger.debug("Extract content for items")
                news_rss_items = []
                for news_item in news_items:
                    rss_items = get_data_for_rss_item(news_item)
                    if "raw_content" in news_item:
                        news_rss_items.append(rss_items)
                news_items = news_rss_items

            if not news_items:
                logger.info(f"> Not found new news in source")
                continue
            else:
                logger.info(f"> Work with {len(news_items)} items")

            resource = source.resource
            language = source.language

            logger.info("Detect digest urls and parse it")

            for item in news_items:
                logger.info(f"Work with {item['link']}")
                # parse weekly digests
                if is_weekly_digest(item):
                    parse_weekly_digest(item)
                    continue

                item.update(
                    {
                        "resource": resource,
                        "language": language,
                    }
                )

                if apply_rules:
                    logger.info("> Apply parsing rules for item")
                    item.update(apply_parsing_rules(item, **kwargs) if kwargs.get("query_rules") else {})
                    logger.debug("> Apply video rules for item")
                    item.update(apply_video_rules(item.copy()))
                logger.info(f"> Save news item - {item['link']}")
                save_news_item(item)
                logger.info(f"> Saved")

        except (URLError, TooManyRedirects, socket.timeout) as e:
            print(source, str(e))


def parsing(func, **kwargs):
    data = {
        "query_rules": ParsingRules.objects.filter(is_activated=True).all(),
        "query_sections": Section.objects.all(),
        "query_statuses": [x[0] for x in ITEM_STATUS_CHOICES],
    }
    if kwargs:
        data.update(**kwargs)
    func(**data)


class Command(BaseCommand):
    args = "no arguments!"
    help = "News import from external resources"

    def handle(self, *args, **options):
        """
        Основной метод - точка входа
        """
        logger.info("Import news from RSS and Twitter")

        apply_rules = False

        parsing(import_tweets, apply_rules=apply_rules)
        parsing(import_rss, apply_rules=apply_rules)
