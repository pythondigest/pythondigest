# -*- coding: utf-8 -*-
import datetime

from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from digest.models import Issue, Item, IssueHabr
from digg_paginator import DiggPaginator

from django.db.models import Q
from django.views.generic import TemplateView, ListView, DetailView, FormView
from django.conf import settings


from .forms import AddNewsForm
from frontend.models import EditorMaterial


class Sitemap(TemplateView):
    content_type = 'text/xml'
    template_name = 'sitemap.html'

    def get_context_data(self, **kwargs):
        ctx = super(Sitemap, self).get_context_data(**kwargs)
        items = [
            {
                'loc': '',
                'changefreq': 'weekly',
            },
            {
                'loc': reverse('frontend:issues'),
                'changefreq': 'weekly',
            },
            {
                'loc': reverse('frontend:feed'),
                'changefreq': 'daily',
            },
        ]

        for issue in Issue.objects.filter(status='active'):
            items.append({
                'loc': issue.link,
                'changefreq': 'weekly',
            })

        ctx.update({
            'records': items,
            'domain': 'http://%s' % settings.BASE_DOMAIN
        })
        return ctx


class Index(DetailView):
    '''
    Главная страница
    '''
    template_name = 'index.html'
    model = Issue
    context_object_name = 'index'
    
    def get_object(self):

        issue = False
        try:
            issue = self.model.objects.filter(status='active').latest('published_at')
        except Issue.DoesNotExist:
            pass

        items = []
        if issue:
            qs = issue.item_set.filter(status='active')
            items = qs.order_by('-section__priority', '-priority')

        return {
            'issue': issue,
            'items': items,
        }


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


class HabrView(DetailView):
    '''
    Рендерер выпуска для публикации на habrahabr.ru
    '''
    template_name = 'issue_habrahabr.html'
    content_type = 'text/plain'
    context_object_name = 'items'

    model = IssueHabr

    def get_context_data(self, **kwargs):

        issue = IssueHabr.objects.get(id=self.kwargs["pk"])

        context = super(HabrView, self).get_context_data()

        items = Item.objects.filter(
            related_to_date__range=(issue.date_from, issue.date_to),
            is_editors_choice=True
        )
        items = items.prefetch_related('issue', 'section')
        items = items.order_by('-created_at', '-related_to_date')

        context.update({
            'items': items
        })

        return context


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
        items = super(NewsList, self).get_queryset().filter(status='active')
        lang = self.request.GET.get('lang')
        if lang in ['ru', 'en']:
            items = items.filter(language=lang)

        search = self.request.GET.get('q')
        if search:
            filters = Q(title__icontains=search) | Q(description__icontains=search)
            items = items.filter(filters)

        section = self.request.GET.get('section')
        if section:
            items = items.filter(section__pk=section)

        items = items.prefetch_related('issue', 'section')
        items = items.order_by('-created_at', '-related_to_date')
        return items

    def get_context_data(self, **kwargs):
        context = super(NewsList, self).get_context_data(**kwargs)
        return context


class AddNews(FormView):
    template_name = "add_news.html"
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
                            section_id=section
                            )
        messages.info(
            self.request, u'Ваша ссылка успешно добавлена на рассмотрение'
        )
        return '/'


class ViewEditorMaterial(TemplateView):
    template_name = 'editor_material_view.html'

    def get_context_data(self, **kwargs):
        section = kwargs.get('section', 'landing')
        slug = kwargs.get('slug')

        material = get_object_or_404(
            EditorMaterial,
            slug=slug,
            section=section,
            status='active'
        )

        return {
            'material': material
        }

class ItemView(DetailView):
    """
    Просмотр отдельной новости
    """
    template_name = 'news_item.html'
    context_object_name = 'item'
    model = Item
