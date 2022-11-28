# -*- encoding: utf-8 -*-

from django.conf import settings


def likes_enable() -> bool:
    return False

    return bool(
        'likes' in settings.INSTALLED_APPS and 'secretballot' in settings.INSTALLED_APPS)
