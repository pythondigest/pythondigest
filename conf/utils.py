from django.conf import settings


def likes_enable() -> bool:
    # TODO: временно отключил голосование, чтобы оптимизировать can_vote в django-likes
    # Сейчас can_vote генерирует по 1 запросу на каждый объект голосования
    # Чтобы определить может человек голосовать или нет
    # Хочется, чтобы делалось 1 запросом это
    return False

    return bool("likes" in settings.INSTALLED_APPS and "secretballot" in settings.INSTALLED_APPS)
