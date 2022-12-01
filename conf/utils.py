from django.conf import settings


def likes_enable() -> bool:
    return bool(
        "likes" in settings.INSTALLED_APPS and "secretballot" in settings.INSTALLED_APPS
    )
