# -*- coding: utf-8 -*-
import datetime

from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from advertising.mixins import AdsMixin
from digest.mixins import FeedItemsMixin, FavoriteItemsMixin
from digest.models import Issue, Item
from frontend.models import EditorMaterial


class Sitemap(TemplateView):
    content_type = 'text/xml'
    template_name = 'sitemap.html'

    def get_context_data(self, **kwargs):
        ctx = super(Sitemap, self).get_context_data(**kwargs)
        items = [
            {'loc': '',
             'changefreq': 'weekly',},
            {'loc': reverse('digest:issues'),
             'changefreq': 'weekly',},
            {'loc': reverse('digest:feed'),
             'changefreq': 'daily',},
        ]

        for issue in Issue.objects.filter(status='active'):
            items.append({'loc': issue.link, 'changefreq': 'weekly',})

        for item in Item.objects.filter(status='active',
                                        activated_at__lte=datetime.datetime.now()):
            items.append(
                {'loc': '/view/%s' % item.pk,
                 'changefreq': 'never',})

        ctx.update(
            {'records': items,
             'domain': 'http://%s' % settings.BASE_DOMAIN})
        return ctx


class IndexView(FavoriteItemsMixin, FeedItemsMixin, AdsMixin, TemplateView):
    """Главная страница."""
    template_name = 'pages/index.html'
    model = Issue
    context_object_name = 'index'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
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

        context.update({
            'issue': issue,
            'items': items,
            'active_menu_item': 'index',
        })
        return context


class FriendsView(TemplateView):
    template_name = 'pages/friends.html'

    def get_context_data(self, **kwargs):
        context = super(FriendsView, self).get_context_data(**kwargs)
        context['active_menu_item'] = 'friends'
        return context


class ViewEditorMaterial(TemplateView):
    template_name = 'old/editor_material_view.html'

    def get_context_data(self, **kwargs):
        section = kwargs.get('section', 'landing')
        slug = kwargs.get('slug')

        material = get_object_or_404(EditorMaterial,
                                     slug=slug,
                                     section=section,
                                     status='active')

        return {'material': material}


