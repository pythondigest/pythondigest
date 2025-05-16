import logging
import random
import re

from bootstrap3.templatetags.bootstrap3 import bootstrap_css_url
from django import template
from django.conf import settings
from django.contrib.messages.utils import get_level_tags
from django.template.defaultfilters import stringfilter
from django.utils.encoding import force_str
from django.utils.translation import get_language, to_locale
from unidecode import unidecode as _unidecode
from urlobject import URLObject

logger = logging.getLogger(__name__)
name_re = re.compile(r"([^O])Auth")
LEVEL_TAGS = get_level_tags()

register = template.Library()


@register.filter
def unidecode(string):
    # last replace is unnecessary, but, for example, in links symbol ' looks awful
    return _unidecode(string.lower().replace(" ", "_")).replace("'", "")


@register.simple_tag()
def locale():
    if settings.LANGUAGE_CODE == "ru-ru":
        return "ru"
    else:
        return to_locale(get_language())


@register.filter
@stringfilter
def trim(value):
    return value.strip()


@register.filter
def empty(value):
    return bool(value)


@register.simple_tag()
def get_message_tags(message):
    """
    Returns the message's level_tag prefixed with Bootstrap's "alert-" prefix
    along with any tags included in message.extra_tags

    Messages in Django >= 1.7 have a message.level_tag attr
    """
    level_tag = force_str(LEVEL_TAGS.get(message.level, ""), strings_only=True)
    if level_tag == "error":
        # Alias the error tag as danger, since .alert-error no longer exists
        # in Bootstrap 3
        level_tag = "danger"

    if level_tag:
        alert_level_tag = f"alert-{level_tag}"
    else:
        alert_level_tag = None

    extra_tags = force_str(message.extra_tags, strings_only=True)

    if extra_tags and alert_level_tag:
        return " ".join([extra_tags, alert_level_tag])
    elif extra_tags:
        return extra_tags
    elif alert_level_tag:
        return alert_level_tag
    return ""


def modify_url_(url, operation, *args):
    """
    Враппер для функций модуля urlobject
    https://urlobject.readthedocs.org/en/latest/quickstart.html
    Назначение: разобрать текщий URL, поменять какую-то его часть и вернуть модифицированный URL в виде строки
    Например: modify_url(some_url, 'del_query_param', 'page') уберет пейджинг из запроса
    Возвращает URL без домена
    """
    if not operation:
        return url

    url = URLObject(url)

    if operation.endswith("_np"):
        url = url.del_query_param("page")
        operation = operation[0:-3]

    op = getattr(url, operation, None)
    if callable(op):
        return str(op(*args))
    raise Exception(f"{operation} is incorrect function name for urlobject.URLObject")


@register.simple_tag(name="money_block_title")
def money_block_title():
    texts = [
        "Покормить редактора",
        "Помочь проекты",
        "Поблагодарить проект",
        "Покормить команду",
        "Помочь оплатить домен",
        "Скинуться на пиво",
        "Скинуться на хостинг",
        "Скинуться на торт",
    ]
    return random.choice(texts)


@register.simple_tag(takes_context=True)
def modify_url(context, operation, *params):
    request = context.get("request")
    params = list(map(str, params))
    if not request:
        return ""

    current_url = request.get_full_path()
    return modify_url_(current_url, operation, *params)


@register.filter
def tags_as_links(tags):
    from digest.models import build_url

    if not tags:
        return list()
    return [(tag.name, build_url("digest:feed", params={"tag": tag.name})) for tag in tags]


@register.filter
def tags_as_str(tags):
    result = "Without tag"

    tags_names = [tag.name for tag in tags]
    if not tags_names:
        return result

    return ",".join(tags_names)


@register.simple_tag()
def bootstrap_url():
    payload = bootstrap_css_url()
    if isinstance(payload, str):
        return payload
    return payload.get("url")


@register.simple_tag()
def jumb_ads():
    items = [
        'и сделали <a href="https://incidenta.tech/?utm_source=pydigest">Тренажер IT-инцидентов для DevOps/SRE</a>',
    ]
    return random.choice(items)
