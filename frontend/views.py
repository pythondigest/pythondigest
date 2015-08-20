# -*- coding: utf-8 -*-
import datetime

from django.conf import settings
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, FormView, ListView, TemplateView

from digest.models import Issue, Item
from digg_paginator import DiggPaginator
from frontend.models import EditorMaterial
from social.backends.utils import load_backends

from .forms import AddNewsForm


class Sitemap(TemplateView):
    content_type = 'text/xml'
    template_name = 'sitemap.html'

    def get_context_data(self, **kwargs):
        ctx = super(Sitemap, self).get_context_data(**kwargs)
        items = [
            {'loc': '',
             'changefreq': 'weekly', },
            {'loc': reverse('frontend:issues'),
             'changefreq': 'weekly', },
            {'loc': reverse('frontend:feed'),
             'changefreq': 'daily', },
        ]

        for issue in Issue.objects.filter(status='active'):
            items.append({'loc': issue.link, 'changefreq': 'weekly', })

        for item in Item.objects.filter(status='active'):
            items.append(
                {'loc': '/view/%s' % item.pk,
                 'changefreq': 'never', })

        ctx.update(
            {'records': items,
             'domain': 'http://%s' % settings.BASE_DOMAIN})
        return ctx


class Index(TemplateView):

    """Главная страница."""
    template_name = 'index.html'
    model = Issue
    context_object_name = 'index'

    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        issue = False
        try:
            issue = self.model.objects.filter(status='active').latest(
                'published_at')
        except Issue.DoesNotExist:
            pass

        items = []
        if issue:
            qs = issue.item_set.filter(status='active')
            items = qs.order_by('-section__priority', '-priority')

        context.update(
            {'issue': issue,
             'items': items,
             'active_menu_item': 'home', })
        return context


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

        context.update({'items': items, 'active_menu_item': 'issue_view'})

        return context


class NewsList(ListView):

    """Лента новостей."""
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


class ViewEditorMaterial(TemplateView):
    template_name = 'editor_material_view.html'

    def get_context_data(self, **kwargs):
        section = kwargs.get('section', 'landing')
        slug = kwargs.get('slug')

        material = get_object_or_404(EditorMaterial,
                                     slug=slug,
                                     section=section,
                                     status='active')

        return {'material': material}


class ItemView(DetailView):

    """Просмотр отдельной новости."""
    template_name = 'news_item.html'
    context_object_name = 'item'
    model = Item
