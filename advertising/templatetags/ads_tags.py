# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import template
from django.core.exceptions import ObjectDoesNotExist

from advertising.models import AdAlign

register = template.Library()


@register.filter
def ads_by_page(ads, page):
    to_remove = []
    for ad in ads:
        for ad_page in ad.pages.all():
            if ad_page.url == page:
                break
        else:
            to_remove.append(ad.id)
    return ads.exclude(id__in=to_remove)


@register.filter
def ads_by_align(ads, align):
    try:
        return ads.filter(align=AdAlign.objects.get(align=align)).first()
    except ObjectDoesNotExist:
        return []
