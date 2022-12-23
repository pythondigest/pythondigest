import logging
import pickle
import random
import re
import time

import requests
from bs4 import BeautifulSoup
from cache_memoize import cache_memoize
from django.conf import settings
from django.core.management import call_command
from readability import Document
from requests.exceptions import InvalidSchema, ProxyError, SSLError
from sentry_sdk import capture_exception
from urllib3.exceptions import ConnectTimeoutError

from digest.models import Item, Section

logger = logging.getLogger(__name__)


def parse_weekly_digest(item_data: dict):
    try:
        if "Python Weekly" in item_data.get("title"):
            logger.info("Run manage command for parse Python Weekly digest")
            call_command("import_python_weekly", item_data.get("link"))

        if item_data.get("link", "").startswith("https://pycoders.com/issues/"):
            logger.info("Run manage command for parse PyCoders Weekly digest")
            call_command("import_pycoders_weekly", item_data.get("link"))

        if item_data.get("link", "").startswith("https://python.libhunt.com/newsletter/"):
            logger.info("Run manage command for parse Awesome Python Weekly digest")
            call_command("import_awesome_python_weekly", item_data.get("link"))
    except Exception as e:
        capture_exception(e)


def is_weekly_digest(item_data: dict) -> bool:
    title = item_data.get("title")
    return bool("Python Weekly" in title)


def _clojure_get_youtube_urls_from_page():
    """
    Замыкание
    Возвращает функцию, которая по коду страницы (requests.text)
        возвращает youtube ссылку
        Применяется для раздела Видео
    :return:
    """
    reg_list = r"((https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(watch\?.*?(?=v=)v=|embed/|v/|.+\?v=)?([^&=%\?]{11}))"

    youtube_links = ["youtu.be", "youtube.com", "youtube-nocookie.com"]

    def form_url(url):
        result = url
        _ = re.findall(reg_list, url)
        if _ and len(_) == 1 and len(_[0]) == 7:
            result = "https://www.youtube.com/watch?v=%s" % _[0][6]
        return result

    def clean_urls(url):
        result = None
        url = re.sub(r"<[^<]+?>", "", url)
        if any(x in url for x in youtube_links):
            result = url.replace(r"//", "") if url.startswith("//") else url
        return result

    def parse_page(content):

        result = None
        try:
            a = filter(lambda x: "youtu" in x, content.split("\n"))
            urls = []
            for x in a:
                _ = re.findall(reg_list, x)
                if _:
                    urls.extend([x[0] for x in filter(lambda x: x and len(x) > 1 and x[0], _)])
                    break

            result = list(
                set(
                    map(
                        form_url,
                        map(clean_urls, filter(lambda x: "%2F" not in x, urls)),
                    )
                )
            )[0]
        except Exception:
            raise
        finally:
            return result

    return parse_page


get_youtube_url_from_page = _clojure_get_youtube_urls_from_page()


def _date_to_julian_day(my_date):
    """
    Returns the Julian day number of a date.
    Origin: http://code-highlights.blogspot.ru/2013/01/julian-date-in-python.html
    :param my_date:
    :return:
    """
    a = (14 - my_date.month) // 12
    y = my_date.year + 4800 - a
    m = my_date.month + 12 * a - 3
    return my_date.day + ((153 * m + 2) // 5) + 365 * y + y // 4 - y // 100 + y // 400 - 32045


def get_readable_content(content):
    return Document(content).summary()


def _get_tags_for_item(item_data: dict, tags_names: list):
    """

    item_data - словарь.
    tags_names - list строк

    значения в словаре item_data, если значение строка
        то сплитится о пробелу и сравнивается с каждым тегом
        если совпадает, то возвращает совпадение

    :param item_data:
    :param tags_names:
    :return:
    """

    try:
        assert isinstance(item_data, dict)
        assert isinstance(tags_names, list)
        return_tags = []
        for _, value in item_data.items():
            if isinstance(value, str) and value:
                return_tags.extend([tag for tag in tags_names if (tag.lower() in value.lower())])
        result = list(set(return_tags))
    except AssertionError:
        result = []
    return result


@cache_memoize(300)  # cache for 5 minutes
def get_https_proxy() -> str | None:
    """Get actual http proxy for requests"""
    proxy_list_url = "https://raw.githubusercontent.com/mertguvencli/http-proxy-list/main/proxy-list/data.txt"

    try:
        response = requests.get(proxy_list_url, timeout=20)
    except requests.Timeout:
        return None

    try:
        response.raise_for_status()
    except requests.HTTPError:
        return None

    proxy_content = response.text
    if not proxy_content:
        return None

    proxy_list = [x.strip() for x in proxy_content.split("\n") if x]
    if not proxy_list:
        return None
    result = random.choice(proxy_list)
    logger.info(f"Get https proxy - {result}")
    return result


def make_get_request(url, timeout=29, try_count=0):
    MAX_RETRIES = 5
    SOFT_SLEEP = 5
    if try_count == MAX_RETRIES:
        logger.info("Too many try for request")
        return None

    requests_kwargs = dict(
        timeout=timeout,
    )

    proxy_https = get_https_proxy()
    if proxy_https and try_count != 0:
        requests_kwargs["proxies"] = {
            "http": proxy_https,
            "https": proxy_https,
        }

    proxy_text = "with" if "proxies" in requests_kwargs else "without"
    logger.info(f"Get data for url {url} {proxy_text} proxy")

    try:
        return requests.get(url, **requests_kwargs)
    except (requests.ConnectTimeout):
        # try again
        logger.info("Timeout error. Try again")
        return make_get_request(url, timeout + 3, try_count + 1)
    except ConnectionResetError:
        if try_count == MAX_RETRIES:
            return None
        time.sleep(SOFT_SLEEP)
        return make_get_request(url, timeout, try_count + 1)
    except (ProxyError, SSLError, ConnectTimeoutError):
        logger.info("Proxy error. Try refresh proxy")
        get_https_proxy.invalidate()
        return make_get_request(url, timeout + 3, try_count + 1)
    except InvalidSchema:
        return None


#
#
# def renew_connection():
#     with control.Controller.from_port(port=9051) as ctl:
#         ctl.authenticate(settings.TOR_CONTROLLER_PWD)
#         ctl.signal(Signal.NEWNYM)
#         sleep(5)
#
#
# def fresh_google_check(link: str, attempt=5, debug=False):
#     """Проверяет, индексировался ли уже ресурс гуглом раньше.
#
#     чем за 2 недели до сегодня.
#     :param link:
#     :param attempt:
#     :return:
#
#     """
#     if debug:
#         return False
#     try:
#         assert isinstance(link, str)
#         today = datetime.date.today()
#         date_s = _date_to_julian_day(today - datetime.timedelta(days=365 * 8))
#         date_e = _date_to_julian_day(today - datetime.timedelta(days=7 * 2))
#         query = 'site:%s daterange:%s-%s' % (link, date_s, date_e,)
#
#         result = False
#         for i in range(0, attempt):
#             g = pygoogle(query.encode('utf-8'),
#                          raise_http_exceptions=True,
#                          proxies=settings.PROXIES_FOR_GOOGLING)
#
#             try:
#                 result = bool(g.get_result_count())
#             except PyGoogleHttpException as e:
#                 renew_connection()
#                 continue
#             break
#     except (AssertionError, PyGoogleHttpException, stem.SocketError):
#         result = False
#
#     return result


def get_tweets_by_url(base_url: str) -> list:
    response = requests.get(base_url, timeout=10)
    soup = BeautifulSoup(response.text, "lxml")
    http_code = response.status_code

    result = []
    for p in soup.findAll("p", "tweet-text"):
        try:
            tw_lnk = p.find("a", "twitter-timeline-link").get("data-expanded-url")
            tw_text = p.contents[0]
            result.append([tw_text, tw_lnk, http_code])
        except Exception as e:
            print("| ", "tweets by url exception", str(e))

    return result


# -------------------
# -------------------
# -------------------
# -------------------
# -------------------
# -------------------


def _check_if_action(if_action: str, if_item: str, if_value: str):
    pattern = re.compile(if_value) if if_action == "regex" else None
    return (
        (if_action == "not_equal" and if_item != if_value)
        or (if_action == "contains" and if_value in if_item)
        or (if_action == "equal" and if_item == if_value)
        or (pattern is not None and pattern.search(if_item) is not None)
    )


def _make_then_action(then_action, rules, sections, statuses, tags):
    query_sections = sections
    query_statuses = statuses
    tags_names = tags

    # ---------------------
    def _make_then_action_set(then_element: str, then_value: str):
        result = {}
        if (then_element == "status" and then_value in query_statuses) or (
            then_element == "section" and query_sections.filter(title=then_value).exists()
        ):
            result = {then_element: then_value}

        if then_element == "http_code" and then_value == "404":
            result = {"status": "moderated"}

        if then_element in ["title", "description"] and then_value:
            result = {then_element: then_value}

        return result

    # ---------------------

    def _make_then_action_add(then_element: str, then_value: str):
        result = {}
        if then_element == "tags" and then_value in tags_names:
            result = {then_element: then_value}

        return result

    # ---------------------

    def _make_then_action_remove_sub_string(then_element: str, then_value: str, if_item: str):
        result = {}

        if then_element in ["title", "description"] and then_value:
            result = {then_element: if_item.replace(then_value, "")}

        return result

    # ---------------------

    functions = {
        "set": _make_then_action_set,
        "add": _make_then_action_add,
        "remove": _make_then_action_remove_sub_string,
    }

    return functions.get(then_action)


def apply_video_rules(item_data: dict) -> dict:
    """
    Применяем правила (захардкоженые) для раздела Видео
    В данном случае если раздел видео, то пытаемся выдрать ссылку на видео
    :param item_data:
    :return:
    """
    youtube_links = ["youtu.be", "youtube.com", "youtube-nocookie.com"]
    result = {}
    if (
        item_data.get("section") == Section.objects.get(title="Видео")
        and all(x not in item_data.get("link") for x in youtube_links)
        and "raw_content" in item_data
    ):
        url = get_youtube_url_from_page(item_data.get("raw_content"))
        if url is not None:
            result["additionally"] = url
    return result


def apply_parsing_rules(item_data: dict, query_rules, query_sections, query_statuses):
    # tags_names = list(query_tags.values_list('name', flat=True))
    tags_names = []
    data = {}

    # _tags_of_item = _get_tags_for_item(item_data, tags_names)
    # if _tags_of_item:
    #     data['tags'] = list(_tags_of_item)

    for rule in query_rules.order_by("-weight"):
        if rule.then_element == "status" and (data.get("status") == "moderated" or data.get("status") == "active"):
            continue
        if rule.then_element == "section" and "section" in data:
            continue

        if_item = item_data.get(rule.if_element, None)
        if if_item is not None:
            if _check_if_action(rule.if_action, if_item, rule.if_value):
                then_element = rule.then_element
                then_action = rule.then_action
                then_value = rule.then_value

                function = _make_then_action(
                    then_action,
                    query_rules,
                    query_sections,
                    query_statuses,
                    tags_names,
                )
                if then_action == "set":
                    data.update(function(then_element, then_value))
                elif then_action == "remove":
                    data.update(function(then_element, then_value, if_item))
                elif then_action == "add":
                    if then_element in data:
                        data[then_element].extend(list(function(then_element, then_value).get(then_element, [])))
                    else:
                        data[then_element] = list(function(then_element, then_value).get(then_element, []))

    # исключений не должно быть,
    # ибо по коду везде очевидно что объект сущесвтует
    # но пускай будет проверка на существование
    if "section" in data:
        try:
            data["section"] = query_sections.get(title=data.get("section"))
        except Exception:
            pass
    # if 'tags' in data:
    #     _tags = []
    #     data['tags'] = list(set(data['tags']))
    #     for x in data['tags']:
    #         try:
    #             _tags.append(query_tags.get(name=x))
    #         except Exception:
    #             pass
    #     data['tags'] = _tags
    return data


# -------------------
# -------------------
# -------------------
# -------------------


def save_news_item(item: dict):
    if not item or item.get("link") is None:
        return

    assert "title" in item
    assert "resource" in item
    assert "link" in item

    if Item.objects.filter(link=item.get("link")).exists():
        return

    try:
        instance, _ = Item.objects.get_or_create(
            title=item.get("title")[:144],
            resource=item.get("resource"),
            link=item.get("link"),
            description=item.get("description", ""),
            status=item.get("status", "autoimport"),
            user_id=settings.BOT_USER_ID,
            section=item.get("section", None),
            additionally=item.get("additionally", None),
            language=item.get("language") if item.get("language") else "en",
        )
    except Exception as e:
        capture_exception(e)
    else:
        if item.get("tags"):
            instance.tags.add(*item.get("tags"))
            instance.save()
        elif item.get("status") == "active":
            instance.save()


def save_pickle_file(filepath, data):
    with open(filepath, "wb") as fio:
        pickle.dump(data, fio)


def load_pickle_file(filepath):
    with open(filepath, "rb") as fio:
        return pickle.load(fio)
