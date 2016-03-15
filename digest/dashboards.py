# -*- encoding: utf-8 -*-
import datetime
from collections import defaultdict

from controlcenter import Dashboard, widgets
from django.conf import settings
from django.db.models import Count
from django.utils import timezone

from .models import Item, Section


class ItemSectionLineChart(widgets.LineChart):
    title = 'Динамика новостей по разделам (месяц)'
    model = Item
    limit_to = 30
    width = widgets.LARGER

    class Chartist:
        options = {
            'axisX': {
                'labelOffset': {
                    'x': -24,
                    'y': 0
                },
            },
            'chartPadding': {
                'top': 24,
                'right': 24,
            }
        }

    def legend(self):
        return Section.objects.all().values_list('title', flat=True)

    def labels(self):
        # По оси `x` дни
        today = timezone.now().date()
        labels = [(today - datetime.timedelta(days=x)).strftime('%d.%m')
                  for x in range(self.limit_to)]
        return labels

    def series(self):
        series = []
        for restaurant in self.legend:
            item = self.values.get(restaurant, {})
            series.append([item.get(label, 0) for label in self.labels])
        return series

    #
    def values(self):
        limit_to = self.limit_to * len(self.legend)
        queryset = self.get_queryset()
        date_field = 'related_to_date' if settings.DEPLOY else 'DATE(related_to_date)'
        queryset = (queryset.filter(status='active')
                    .extra({'baked':
                                date_field})
                    .select_related('section')
                    .values_list('section__title', 'baked')
                    .order_by('-baked')
                    .annotate(ocount=Count('pk'))[:limit_to])

        values = defaultdict(dict)
        for restaurant, date, count in queryset:
            day_month = '{2}.{1}'.format(*date.split('-'))
            values[restaurant][day_month] = count
        return values


class ItemSingleBarChart(widgets.SingleBarChart):
    # Строит бар-чарт по числу заказов
    title = 'Новости по неделям'
    model = Item
    limit_to = 30
    width = widgets.LARGER

    class Chartist:
        options = {
            # По-умолчанию, Chartist может использовать
            # float как промежуточные значения, это ни к чему
            'onlyInteger': True,
            # Внутренние отступы чарта -- косметика
            'chartPadding': {
                'top': 24,
                'right': 0,
                'bottom': 0,
                'left': 0,
            }
        }

    def values(self):
        queryset = self.get_queryset()

        date_field = 'related_to_date' if settings.DEPLOY else 'DATE(related_to_date)'
        return (queryset.extra({'baked':date_field})
                .values_list('baked')
                .order_by('-baked')
                .annotate(ocount=Count('pk'))[:self.limit_to])


class MyDashboard(Dashboard):
    widgets = (
        ItemSectionLineChart,
        ItemSingleBarChart,
    )
