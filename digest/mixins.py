# -*- encoding: utf-8 -*-
import datetime
import random

from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.utils.cache import patch_response_headers
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page, never_cache
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import ContextMixin

from conf.utils import likes_enable
from digest.models import Item


def get_feed_items(count=10):
    return Item.objects.filter(
        status='active',
        activated_at__lte=datetime.datetime.now()
    ).prefetch_related('issue', 'section').order_by('-created_at',
                                                    '-related_to_date')[:count]


class FeedItemsMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super(FeedItemsMixin, self).get_context_data(**kwargs)
        context['feed_items'] = get_feed_items(15)
        return context


class FavoriteItemsMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super(FavoriteItemsMixin, self).get_context_data(**kwargs)

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
            items = Item.objects.filter(
                id__in=set(Vote.objects.filter(
                    content_type=ContentType.objects.get(app_label='digest',
                                                         model='item'),
                ).values_list('object_id', flat=True)),
                related_to_date__gt=date)
            items_score = [(item, item.vote_total) for item in items if
                           item.vote_total > 0]
            items_score = sorted(items_score, key=lambda item: item[1],
                                 reverse=True)
            context['favorite_items'] = [x[0] for x in items_score[:10]]
        return context


class NeverCacheMixin(object):
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        return super(NeverCacheMixin, self).dispatch(*args, **kwargs)


class LoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)


class CSRFExemptMixin(object):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(CSRFExemptMixin, self).dispatch(*args, **kwargs)


class CacheMixin(object):
    cache_timeout = 60

    def get_cache_timeout(self):
        return self.cache_timeout

    def dispatch(self, *args, **kwargs):
        return cache_page(self.get_cache_timeout())(
            super(CacheMixin, self).dispatch)(*args, **kwargs)


class CacheControlMixin(object):
    cache_timeout = 60

    def get_cache_timeout(self):
        return self.cache_timeout

    def dispatch(self, *args, **kwargs):
        response = super(CacheControlMixin, self).dispatch(*args, **kwargs)
        patch_response_headers(response, self.get_cache_timeout())
        return response


class JitterCacheMixin(CacheControlMixin):
    cache_range = [40, 80]

    def get_cache_range(self):
        return self.cache_range

    def get_cache_timeout(self):
        return random.randint(*self.get_cache_range())
