# -*- coding: utf-8 -*-

import datetime

from concurrency.views import ConflictResponse
from digg_paginator import DiggPaginator
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import JsonResponse
from django.template import loader
from django.template.context import RequestContext
from django.views.generic import DetailView
from django.views.generic import FormView, ListView

from advertising.mixins import AdsMixin
from .forms import AddNewsForm
from .mixins import FeedItemsMixin, CacheMixin, FavoriteItemsMixin
from .models import Issue, Item


def conflict(request, target=None, template_name='409.html'):
    template = loader.get_template(template_name)
    message = 'Вот незадача! Кажется эту новость обновили раньше =( \
            Нужно обновить новость для того чтобы внести правки.'

    ctx = RequestContext(request, {'message': message})
    return ConflictResponse(template.render(ctx))


class IssuesList(CacheMixin, ListView):
    """Список выпусков."""
    template_name = 'digest/pages/issues_list.html'
    queryset = Issue.objects.filter(status='active').order_by('-published_at')
    context_object_name = 'items'
    paginate_by = 12
    paginator_class = DiggPaginator
    cache_timeout = 300

    def get_context_data(self, **kwargs):
        context = super(IssuesList, self).get_context_data(**kwargs)
        context['active_menu_item'] = 'issues_list'
        return context


class IssueView(CacheMixin, FavoriteItemsMixin, FeedItemsMixin, AdsMixin, DetailView):
    """Просмотр выпуска."""
    template_name = 'digest/pages/issue.html'
    model = Issue
    cache_timeout = 300

    def get_context_data(self, **kwargs):
        context = super(IssueView, self).get_context_data(**kwargs)

        items = self.object.item_set.filter(status='active').order_by(
            '-section__priority', '-priority')

        context.update({
            'items': items,
            'active_menu_item': 'issue_view',
        })

        return context


class ItemView(FavoriteItemsMixin, CacheMixin, DetailView):
    """Просмотр отдельной новости."""
    template_name = 'digest/pages/news_item.html'
    context_object_name = 'item'
    model = Item
    cache_timeout = 300


class ItemsByTagView(AdsMixin, FavoriteItemsMixin, CacheMixin, ListView):
    """Лента новостей."""
    template_name = 'news_by_tag.html'
    context_object_name = 'items'
    paginate_by = 20
    paginator_class = DiggPaginator
    model = Item
    cache_timeout = 300

    def get_queryset(self):
        items = super(ItemsByTagView, self).get_queryset() \
            .filter(status='active',
                    activated_at__lte=datetime.datetime.now())
        tag = self.request.GET.get('tag')
        if tag in ['ru', 'en']:
            items = items.filter(tags__name__in=tag)

        items = items.prefetch_related('issue', 'section')
        items = items.order_by('-created_at', '-related_to_date')
        return items


class NewsList(FavoriteItemsMixin, CacheMixin, ListView):
    """Лента новостей."""
    template_name = 'digest/pages/news_list.html'
    context_object_name = 'items'
    paginate_by = 20
    paginator_class = DiggPaginator
    model = Item
    cache_timeout = 300

    def get_queryset(self):
        items = super(NewsList, self).get_queryset() \
            .filter(status='active',
                    activated_at__lte=datetime.datetime.now())
        lang = self.request.GET.get('lang')
        if lang in ['ru', 'en']:
            items = items.filter(language=lang)

        search = self.request.GET.get('q')
        if search:
            filters = Q(title__icontains=search) | Q(
                description__icontains=search)
            items = items.filter(filters)

        tag = self.request.GET.get('tag')
        if tag:
            items = items.filter(tags__name__in=[tag])

        section = self.request.GET.get('section', '')
        if section.isdigit():
            items = items.filter(section__pk=section)

        items = items.prefetch_related('issue', 'section')
        items = items.order_by('-created_at', '-related_to_date')
        return items

    def get_context_data(self, **kwargs):
        context = super(NewsList, self).get_context_data(**kwargs)
        context['active_menu_item'] = 'feed'
        return context


class AddNews(FormView):
    template_name = 'digest/pages/add_news.html'
    form_class = AddNewsForm

    def get_success_url(self):
        title = self.request.POST['title'].strip() or 'Без заголовка'
        link = self.request.POST['link']
        description = self.request.POST['description']
        section = self.request.POST['section']
        Item.objects.create(title=title,
                            link=link,
                            description=description,
                            status='pending',
                            related_to_date=datetime.datetime.now(),
                            section_id=section)
        messages.info(self.request,
                      u'Ваша ссылка успешно добавлена на рассмотрение')
        return reverse('frontend:index')


def get_items_json(request, year, month, day):
    result = {}
    items = Item.objects.filter(
        status='active',
        is_editors_choice=True,
        related_to_date__year=int(year),
        related_to_date__month=int(month),
        related_to_date__day=int(day),
    )
    result['ok'] = bool(items)
    if items:
        keys = [
            'title',
            'description',
            'section__title',
            'link',
            'language',
        ]
        result['items'] = list(items.values(*keys))
    return JsonResponse(result)
