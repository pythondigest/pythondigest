# -*- coding: utf-8 -*-

import datetime

from concurrency.views import ConflictResponse
from digg_paginator import DiggPaginator
from django.contrib import messages
from django.db.models import Q
from django.template import loader
from django.template.context import RequestContext
from django.views.generic import DetailView
from django.views.generic import FormView, ListView

from advertising.models import get_ads
from digest.models import Issue, Item
from .forms import AddNewsForm


def conflict(request, target=None, template_name='409.html'):
    template = loader.get_template(template_name)
    message = 'Вот незадача! Кажется эту новость обновили раньше =( \
            Нужно обновить новость для того чтобы внести правки.'

    ctx = RequestContext(request, {'message': message})
    return ConflictResponse(template.render(ctx))


class IssuesList(ListView):
    """Список выпусков."""
    template_name = 'issues_list.html'
    queryset = Issue.objects.filter(status='active').order_by('-published_at')
    context_object_name = 'items'
    paginate_by = 9
    paginator_class = DiggPaginator

    def get_context_data(self, **kwargs):
        context = super(IssuesList, self).get_context_data(**kwargs)
        context['active_menu_item'] = 'issues_list'
        return context


class IssueView(DetailView):
    """Просмотр выпуска."""
    template_name = 'issue.html'
    model = Issue

    def get_context_data(self, **kwargs):
        context = super(IssueView, self).get_context_data(**kwargs)

        items = self.object.item_set.filter(status='active').order_by(
            '-section__priority', '-priority')

        context.update({
            'items': items,
            'active_menu_item': 'issue_view',
            'ads': get_ads()})

        return context


class ItemView(DetailView):
    """Просмотр отдельной новости."""
    template_name = 'news_item.html'
    context_object_name = 'item'
    model = Item


class NewsList(ListView):
    """Лента новостей."""
    template_name = 'news_list.html'
    context_object_name = 'items'
    paginate_by = 20
    paginator_class = DiggPaginator
    model = Item

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
    template_name = 'add_news.html'
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
        return '/'
