# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
import random
import re

import lxml.html
from django import template
from django.conf import settings
from django.contrib.messages.utils import get_level_tags
from django.utils.encoding import force_text
from django.utils.six import text_type
from django.utils.translation import to_locale, get_language
from social.backends.oauth import OAuthAuth
from social.backends.utils import load_backends
from unidecode import unidecode as _unidecode
from urlobject import URLObject

logger = logging.getLogger(__name__)
name_re = re.compile(r'([^O])Auth')
LEVEL_TAGS = get_level_tags()

register = template.Library()


@register.filter
def unidecode(string):
    return _unidecode(string.lower().replace(" ", "_")).replace("'",
                                                                "")  # last replace is unnecessary, but, for example, in links symbol ' looks awful


@register.filter
def remove_classes(text):
    html = lxml.html.fromstring(text)
    for tag in html.xpath('//*[@class]'):
        tag.attrib.pop('class')

    return lxml.html.tostring(html)


@register.simple_tag()
def locale():
    if settings.LANGUAGE_CODE == 'ru-ru':
        return 'ru'
    else:
        return to_locale(get_language())


@register.simple_tag()
def get_message_tags(message):
    """
    Returns the message's level_tag prefixed with Bootstrap's "alert-" prefix
    along with any tags included in message.extra_tags

    Messages in Django >= 1.7 have a message.level_tag attr
    """
    level_tag = force_text(LEVEL_TAGS.get(message.level, ''),
                           strings_only=True)
    if level_tag == 'error':
        # Alias the error tag as danger, since .alert-error no longer exists
        # in Bootstrap 3
        level_tag = 'danger'

    if level_tag:
        alert_level_tag = 'alert-{tag}'.format(tag=level_tag)
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
    raise Exception('%s is incorrect function name for urlobject.URLObject' %
                    operation)


@register.simple_tag(name='money_block_title')
def money_block_title():
    texts = [
        'Покормить редактора',
        'Помочь проекты',
        'Поблагодарить проект',
        'Покормить команду',
        'Помочь оплатить домен',
        'Скинуться на пиво',
        'Скинуться на хостинг',
        'Скинуться на торт',
    ]
    return random.choice(texts)


@register.simple_tag(takes_context=True)
def modify_url(context, operation, *params):
    request = context.get('request')
    params = list(map(str, params))
    if not request:
        return u''

    current_url = request.get_full_path()
    return modify_url_(current_url, operation, *params)


@register.filter
def backend_name(backend):
    name = backend.__class__.__name__
    name = name.replace('OAuth', ' OAuth')
    name = name.replace('OpenId', ' OpenId')
    name = name.replace('Sandbox', '')
    name = name_re.sub(r'\1 Auth', name)
    return name


@register.filter
def backend_class(backend):
    return backend.name.replace('-', ' ')


@register.filter
def icon_name(name):
    return {
        'stackoverflow': 'stack-overflow',
        'google-oauth': 'google',
        'google-oauth2': 'google',
        'google-openidconnect': 'google',
        'yahoo-oauth': 'yahoo',
        'facebook-app': 'facebook',
        'email': 'envelope',
        'vimeo': 'vimeo-square',
        'linkedin-oauth2': 'linkedin',
        'vk-oauth2': 'vk',
        'live': 'windows',
        'username': 'user',
    }.get(name, name)


@register.assignment_tag
def get_available_backends():
    return load_backends(settings.AUTHENTICATION_BACKENDS)


@register.filter
def social_backends(backends):
    backends = [(name, backend) for name, backend in backends.items()
                if name not in ['username', 'email']]
    backends.sort(key=lambda b: b[0])
    return [backends[n:n + 10] for n in range(0, len(backends), 10)]


@register.filter
def legacy_backends(backends):
    backends = [(name, backend) for name, backend in backends.items()
                if name in ['username', 'email']]
    backends.sort(key=lambda b: b[0])
    return backends


@register.filter
def oauth_backends(backends):
    backends = [(name, backend) for name, backend in backends.items()
                if issubclass(backend, OAuthAuth)]
    backends.sort(key=lambda b: b[0])
    return backends


@register.simple_tag(takes_context=True)
def associated(context, backend):
    user = context.get('user')
    context['association'] = None
    if user and user.is_authenticated():
        try:
            context['association'] = user.social_auth.filter(
                provider=backend.name)[0]
        except IndexError as e:
            logger.warning(e)
    return ''
