#!/usr/bin/env python
#
# Copyright 2018 Tyndyll
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# https://gist.github.com/tyndyll/e254ae3da2d0427371733443152c1337

from urllib.parse import parse_qs, urlencode, urlparse

params_to_remove = [
    "mkt_tok",
    "utm_source",  # identifies which site sent the traffic, and is a required parameter
    "utm_medium",  # identifies what type of link was used, such as cost per click or email
    "utm_campaign",  # 	identifies a specific product promotion or strategic campaign
    "utm_term",  # identifies search terms
    "utm_content",  # identifies what specifically was clicked to bring the user to the site
    "sc_country",
    "sc_category",
    "sc_channel",
    "sc_campaign",
    "sc_publisher",
    "sc_content",
    "sc_funnel",
    "sc_medium",
    "sc_segment",
]


def remove_tracker_params(query_string):
    """
    Given a query string from a URL, strip out the known trackers

    >>> remove_tracker_params("utm_campaign=2018-05-31&utm_medium=email&utm_source=courtside-20180531")
    ''

    >>> remove_tracker_params("a=b&utm_campaign=2018-05-31&utm_medium=email&utm_source=courtside-20180531")
    'a=b'

    >>> remove_tracker_params("type=test&type=test2")
    'type=test&type=test2'
    """

    params = []
    for param, values in parse_qs(query_string).items():
        if param not in params_to_remove:
            # value will be a list, extract each one out
            for value in values:
                params.append((param, value))
    return urlencode(params)


def clean_url(url):
    """
    Given a URL, return it with the UTM parameters removed

    >>> clean_url("https://dribbble.com/stories/2018/05/29/an-interview-with-user-interface-designer-olga?utm_campaign=2018-05-31&utm_medium=email&utm_source=courtside-20180531")
    'https://dribbble.com/stories/2018/05/29/an-interview-with-user-interface-designer-olga'

    It will also clean the UTM parameters from fragments

    >>> clean_url("https://blog.mozvr.com/introducing-hubs-a-new-way-to-get-together-online/?sample_rate=0.001#utm_source=desktop-snippet&utm_medium=snippet&utm_campaign=MozillaHubsIntro&utm_term=8322&utm_content=PRE")
    'https://blog.mozvr.com/introducing-hubs-a-new-way-to-get-together-online/?sample_rate=0.001'
    """

    parsed = urlparse(url)
    parsed = parsed._replace(query=remove_tracker_params(parsed.query))
    parsed = parsed._replace(fragment=remove_tracker_params(parsed.fragment))
    return parsed.geturl()
