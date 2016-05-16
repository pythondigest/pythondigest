# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
import re

import requests
from django import template
from django.contrib.messages.utils import get_level_tags

logger = logging.getLogger(__name__)
name_re = re.compile(r'([^O])Auth')
LEVEL_TAGS = get_level_tags()

register = template.Library()

RSS2JSON_URLS = [
    'https://ajax.googleapis.com/ajax/services/feed/load?v=2.0&q={}&num=20',
    'http://rss2json.com/api.json?rss_url={}',
]


@register.assignment_tag
def rss2json(url):
    result = {}
    try:
        resp = requests.get(RSS2JSON_URLS[0].format(url))
        return resp.json()
    except Exception as e:
        print(e)
        pass
    return result


@register.assignment_tag
def rss2libraries(url):
    items = []
    json = rss2json(url)
    if 'items' in json:
        items = json.get('items', [])
    elif 'responseData' in json:
        items = json.get('responseData', {}) \
            .get('feed', {}) \
            .get("entries", [])
    return items
