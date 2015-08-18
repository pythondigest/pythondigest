# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from urlobject import URLObject

from django.utils.six import text_type
from django import template
from django.contrib.messages.utils import get_level_tags
from django.utils.encoding import force_text

LEVEL_TAGS = get_level_tags()

register = template.Library()


@register.simple_tag()
def get_message_tags(message):
    """
    Returns the message's level_tag prefixed with Bootstrap's "alert-" prefix
    along with any tags included in message.extra_tags

    Messages in Django >= 1.7 have a message.level_tag attr
    """
    level_tag = force_text(LEVEL_TAGS.get(message.level, ''), strings_only=True)
    if level_tag == "error":
        # Alias the error tag as danger, since .alert-error no longer exists
        # in Bootstrap 3
        level_tag = "danger"

    if level_tag:
        alert_level_tag = "alert-{tag}".format(tag=level_tag)
    else:
        alert_level_tag = None

    extra_tags = force_text(message.extra_tags, strings_only=True)

    if extra_tags and alert_level_tag:
        return ' '.join([extra_tags, alert_level_tag])
    elif extra_tags:
        return extra_tags
    elif alert_level_tag:
        return alert_level_tag
    return ''

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

    if operation.endswith('_np'):
        url = url.del_query_param('page')
        operation = operation[0:-3]

    op = getattr(url, operation, None)
    if callable(op):
        return text_type(op(*args))
    raise Exception('%s is incorrect function name for urlobject.URLObject' % operation)

@register.simple_tag(takes_context=True)
def modify_url(context, operation, *params):
    request = context.get('request')
    params = list(map(str, params))
    if not request:
        return u''

    current_url = request.get_full_path()
    return modify_url_(current_url, operation, *params)