import datetime
import random

from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.db.models import Count, Q, Sum
from django.utils.cache import patch_response_headers
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page, never_cache
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import ContextMixin

from conf.utils import likes_enable
from digest.models import Item


def get_feed_items(count=10):
    return (
        Item.objects.filter(
            status="active",
            activated_at__lte=datetime.datetime.now(),
            activated_at__gte=datetime.datetime.now() - datetime.timedelta(days=90),
        )
        .exclude(section=None)
        .prefetch_related("issue", "section", "tags")
        .order_by("-created_at", "-related_to_date")[:count]
    )


class FeedItemsMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["feed_items"] = get_feed_items(15)
        return context


class FavoriteItemsMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # вариант1
        # Получить все голоса
        # Сгруппировать по Item
        # Из всех объектов голосов выгрузить значение
        # Определить total
        # Выбрать лучшие

        # вариант2
        # Получить все голоса
        # Получить по ним сет из Item (без дублей)
        # пройтись по всем и сформировать лист

        if likes_enable():
            from secretballot.models import Vote

            date = datetime.datetime.now() - datetime.timedelta(days=12)
            items = (
                Item.objects.filter(
                    status="active",
                    related_to_date__gt=date,
                )
                .exclude(section=None)
                .annotate(
                    q_vote_total=Sum(
                        "votes__vote",
                    )
                )
                .filter(q_vote_total__gte=0)
                .prefetch_related("tags", "votes")
            )

            items_score = [
                (item, item.q_vote_total) for item in items if item.q_vote_total >= 0
            ]
            items_score = sorted(items_score, key=lambda item: item[1], reverse=True)
            context["favorite_items"] = [x[0] for x in items_score[:10]]
        return context


class NeverCacheMixin:
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class LoginRequiredMixin:
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class CSRFExemptMixin:
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class CacheMixin:
    cache_timeout = 60

    def get_cache_timeout(self):
        return self.cache_timeout

    def dispatch(self, *args, **kwargs):
        return cache_page(self.get_cache_timeout())(super().dispatch)(*args, **kwargs)


class CacheControlMixin:
    cache_timeout = 60

    def get_cache_timeout(self):
        return self.cache_timeout

    def dispatch(self, *args, **kwargs):
        response = super().dispatch(*args, **kwargs)
        patch_response_headers(response, self.get_cache_timeout())
        return response


class JitterCacheMixin(CacheControlMixin):
    cache_range = [40, 80]

    def get_cache_range(self):
        return self.cache_range

    def get_cache_timeout(self):
        return random.randint(*self.get_cache_range())
