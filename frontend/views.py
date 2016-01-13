# -*- coding: utf-8 -*-
import datetime

from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

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
                 'active_menu_item': 'home',})
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


def get_items_json(request, year, month, day):
    result = {}
    items = Item.objects.filter(
            status='active',
            is_editors_choice=True,
            activated_at__year=int(year),
            activated_at__month=int(month),
            activated_at__day=int(day),
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
