# -*- coding: utf-8 -*-

from urllib.parse import parse_qs, urlparse

from django import template

register = template.Library()


@register.simple_tag(name='youtube_id')
def youtube_id(value):
    """
    Examples:

    >>> youtube_id("http://youtu.be/SA2iWivDJiE")
    SA2iWivDJiE
    >>> youtube_id("http://www.youtube.com/watch?v=_oPAwA_Udwc&feature=feedu")
    _oPAwA_Udwc
    >>> youtube_id("http://www.youtube.com/embed/SA2iWivDJiE")
    SA2iWivDJiE
    >>> youtube_id("http://www.youtube.com/v/SA2iWivDJiE?version=3&amp;hl=en_US")
    SA2iWivDJiE
    """
    query = urlparse(value)
    if query.hostname == 'youtu.be':
        return query.path[1:]
    if query.hostname in ('www.youtube.com', 'youtube.com'):
        if query.path == '/watch':
            p = parse_qs(query.query)
            return p['v'][0]
        if query.path[:7] == '/embed/':
            return query.path.split('/')[2]
        if query.path[:3] == '/v/':
            return query.path.split('/')[2]
    # fail?
    return None


youtube_links = ['youtu.be', 'youtube.com', 'youtube-nocookie.com']


@register.filter(name='is_youtube')
def is_youtube(url):
    return any(x in url for x in youtube_links)
