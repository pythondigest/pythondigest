# -*- coding: utf-8 -*-
# Create your views here.
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView
from digest.models import Issue, Item
from digg_paginator import DiggPaginator
from syncrss.models import RawItem



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
    queryset = Item.objects.filter(status='active').prefetch_related('issue', 'section').order_by('-created_at')
    context_object_name = 'items'
    paginate_by = 20
    paginator_class = DiggPaginator

    def get_context_data(self, *args, **kwargs):
        context = super(NewsList, self).get_context_data(*args, **kwargs)
        context['itemsrss'] = RawItem.objects.filter(status='active')
        return context

    def get_queryset(self):
        qs = super(NewsList, self).get_queryset()
        lang = self.request.GET.get('lang')
        if lang in ['ru', 'en']:
            qs = qs.filter(language=lang)
        return qs
