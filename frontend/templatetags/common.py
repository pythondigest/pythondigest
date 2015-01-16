# -*- coding: utf8 -*-
from urlobject import URLObject

from django import template

register = template.Library()


def modify_url_(url, operation, *args):
    '''
    Враппер для функций модуля urlobject
    https://urlobject.readthedocs.org/en/latest/quickstart.html
    Назначение: разобрать текщий URL, поменять какую-то его часть и вернуть модифицированный URL в виде строки
    Например: modify_url(some_url, 'del_query_param', 'page') уберет пейджинг из запроса
    Возвращает URL без домена
    '''
    if not operation:
        return url

    url = URLObject(url)

    if operation.endswith('_np'):
        url = url.del_query_param('page')
        operation = operation[0:-3]

    op = getattr(url, operation, None)
    if callable(op):
        return unicode(op(*args))
    raise Exception('%s is incorrect function name for urlobject.URLObject' % operation)

@register.simple_tag(takes_context=True)
def modify_url(context, operation, *params):
    request = context.get('request')
    params = list(map(str, params))
    if not request:
        return u''

    current_url = request.get_full_path()
    return modify_url_(current_url, operation, *params)