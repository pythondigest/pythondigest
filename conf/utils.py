# -*- encoding: utf-8 -*-

from django.conf import settings


def likes_enable() -> bool:
    return bool('likes' and 'secretballot' in settings.INSTALLED_APPS)
