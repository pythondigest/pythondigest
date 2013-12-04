# -*- coding: utf-8 -*-
# Create your views here.
from django.shortcuts import get_object_or_404, render_to_response
from django.views.generic import TemplateView, ListView, DetailView, FormView
from digest.models import Issue, Item
from digg_paginator import DiggPaginator
from django.db.models import Q
from django.template import RequestContext
from .forms import SearchForm

class Index(TemplateView):
    '''
    Главная страница
    '''
    template_name = 'index.html'


class IssuesList(ListView):
    '''
    Список выпусков
    '''
    template_name = 'issues_list.html'
    queryset = Issue.objects.filter(status='active').order_by('-published_at')
    context_object_name = 'items'
    paginate_by = 9
    paginator_class = DiggPaginator


class IssueView(DetailView):
    '''
    Просмотр выпуска
    '''
    template_name = 'issue.html'
    model = Issue

    def get_context_data(self, **kwargs):
        context = super(IssueView, self).get_context_data(**kwargs)

        items = self.object.item_set.filter(status='active').order_by('-section__priority', '-priority')

        context.update({
            'items': items
        })

        return context

class HabrView(IssueView):
    '''
    Рендерер выпуска для публикации на habrahabr.ru
    '''
    template_name = 'issue_habrahabr.html'
    content_type = 'text/plain'


class NewsList(ListView):
    '''
    Лента новостей
    '''
    template_name = 'news_list.html'
    context_object_name = 'items'
    paginate_by = 20
    paginator_class = DiggPaginator
    model = Item

    def get_queryset(self):
        items = super(NewsList, self).get_queryset()
        lang = self.request.GET.get('lang')
        if lang in ['ru', 'en']:
            items = items.filter(language=lang)
        print lang
        if 'q' in self.request.GET and self.request.GET['q']:
            search = self.request.GET['q']
            items = items.filter(Q(title__icontains=search)| \
                                 Q(descripton__icontains=search))
        else:
            items = items.filter(status='active'). \
                            prefetch_related('issue', 'section'). \
                            order_by('-created_at', '-related_to_date')
        return items

    def get_context_data(self, **kwargs):
        context = super(NewsList, self).get_context_data(**kwargs)
        context['form'] = SearchForm()
        return context
