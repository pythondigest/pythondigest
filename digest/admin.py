# -*- coding: utf-8 -*-
import logging
from datetime import datetime, timedelta

from django import forms
from django.contrib import admin
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.html import escape

from conf.utils import likes_enable
from digest.forms import ItemStatusForm
from digest.models import AutoImportResource, Issue, Item, Package, \
    ParsingRules, Resource, Section, get_start_end_of_week, ItemClsCheck
from digest.pub_digest import pub_to_all

logger = logging.getLogger(__name__)
admin.site.unregister(Site)


def link_html(obj):
    link = escape(obj.link)
    return '<a target="_blank" href="%s">%s</a>' % (link, link)


def _save_item_model(request, item: Item, form, change) -> None:
    prev_status = False
    if not item.pk:
        item.user = request.user
        if not item.issue:
            la = lna = False
            qs = Issue.objects
            try:
                # последний активный
                la = qs.filter(status='active').order_by('-pk')[0:1].get()
                # последний неактивный
                lna = qs.filter(pk__gt=la.pk).order_by('pk')[0:1].get()
            except Issue.DoesNotExist as e:
                logger.warning('Not found last or recent issue')

            if la or lna:
                item.issue = lna or la
    else:
        old_obj = Item.objects.get(pk=item.pk)
        prev_status = old_obj.status

    # Обновление времени модификации при смене статуса на активный
    new_status = form.cleaned_data.get('status')
    if not prev_status == 'active' and new_status == 'active':
        item.modified_at = datetime.now()


def _external_link(obj):
    lnk = escape(obj.link)
    ret = '<a target="_blank" href="%s">Ссылка&nbsp;&gt;&gt;&gt;</a>' % lnk
    username = obj.user.username if obj.user else 'Гость'
    ret = '%s<br>Добавил: %s' % (ret, username)
    return ret


class IssueAdmin(admin.ModelAdmin):
    list_display = ('title', 'news_count', 'issue_date', 'frontend_link',)

    list_filter = ('date_from', 'date_to',)

    exclude = ('last_item', 'version',)
    actions = ['make_published']

    def issue_date(self, obj):
        return 'С %s по %s' % (obj.date_from, obj.date_to)

    issue_date.short_description = 'Период'

    def news_count(self, obj):
        return '%s' % Item.objects.filter(issue__pk=obj.pk,
                                           status='active').count()

    news_count.short_description = 'Количество новостей'

    def frontend_link(self, obj):
        lnk = reverse('digest:issue_view', kwargs={'pk': obj.pk})
        return '<a target="_blank" href="%s">%s</a>' % (lnk, lnk)

    frontend_link.allow_tags = True
    frontend_link.short_description = 'Просмотр'

    def make_published(self, request, queryset):
        from django_q.tasks import async

        if len(queryset) == 1:
            issue = queryset[0]
            site = 'http://pythondigest.ru'
            async(
                pub_to_all,
                issue.announcement,
                '{0}{1}'.format(site, issue.link),
                '{0}{1}'.format(site, issue.image.url if issue.image else '')
            )

    make_published.short_description = 'Опубликовать анонс в социальные сети'


admin.site.register(Issue, IssueAdmin)


class SectionAdmin(admin.ModelAdmin):
    ordering = ('-priority',)


admin.site.register(Section, SectionAdmin)


class ParsingRulesAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_activated', 'weight', 'if_element',
                    '_get_if_action', 'then_element', '_get_then_action',)

    list_filter = ('is_activated', 'if_element', 'if_action', 'then_element',
                   'then_action',)

    list_editable = ('is_activated',)

    search_fields = ('is_activated', 'title', 'if_value', 'then_value',)

    def _get_if_action(self, obj):
        return '{0}: <i>{1}</i>'.format(
            obj.get_if_action_display(),
            obj.if_value)

    _get_if_action.allow_tags = True
    _get_if_action.short_description = 'Условие'

    def _get_then_action(self, obj):
        return '{0}: <i>{1}</i>'.format(obj.get_then_action_display(),
                                         obj.then_value)

    _get_then_action.allow_tags = True
    _get_then_action.short_description = 'Действие'


admin.site.register(ParsingRules, ParsingRulesAdmin)


class ItemAdmin(admin.ModelAdmin):
    # form = ItemStatusForm
    fields = (
        'section',
        'title',
        'is_editors_choice',
        'description',
        'issue',
        'link',
        'status',
        'language',
        'tags',
        'keywords',
        'additionally',

    )
    # filter_horizontal = ('tags',)
    list_filter = ('status', 'issue', 'section', 'is_editors_choice', 'user',
                   'related_to_date', 'resource',)
    search_fields = ('title', 'description', 'link', 'resource__title')
    list_display = ('title', 'section', 'status', 'external_link',
                    'related_to_date', 'is_editors_choice', 'resource',)

    list_editable = ('is_editors_choice', 'section')
    exclude = ('modified_at',),
    radio_fields = {'language': admin.HORIZONTAL, 'status': admin.HORIZONTAL,}

    external_link = lambda s, obj: _external_link(obj)
    external_link.allow_tags = True
    external_link.short_description = 'Ссылка'

    def save_model(self, request, obj, form, change):
        _save_item_model(request, obj, form, change)
        super(ItemAdmin, self).save_model(request, obj, form, change)


admin.site.register(Item, ItemAdmin)


class ResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'link_html')

    link_html = lambda s, obj: link_html(obj)
    link_html.allow_tags = True
    link_html.short_description = 'Ссылка'


admin.site.register(Resource, ResourceAdmin)


class AutoImportResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'link_html', 'type_res', 'resource', 'incl',
                    'excl', 'in_edit', 'language')
    formfield_overrides = {
        models.TextField: {
            'widget': forms.Textarea(attrs={'cols': 45,
                                            'rows': 1})
        },
    }

    link_html = lambda s, obj: link_html(obj)
    link_html.allow_tags = True
    link_html.short_description = 'Ссылка'


admin.site.register(AutoImportResource, AutoImportResourceAdmin)


class PackageAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'link'
    )


admin.site.register(Package, PackageAdmin)


class ItemModerator(Item):
    class Meta:
        proxy = True
        verbose_name_plural = 'Новости (эксперимент)'


class ItemModeratorAdmin(admin.ModelAdmin):
    form = ItemStatusForm
    fields = (
        'section',
        'title',
        'is_editors_choice',
        'description',
        'external_link_edit',
        'status',
        'language',
        'tags',
        'activated_at',
    )

    readonly_fields = ('external_link_edit',)
    list_display = ('title', 'status', 'external_link', 'cls_ok',
                    'activated_at')

    exclude = ('modified_at',),
    radio_fields = {'language': admin.HORIZONTAL, 'status': admin.HORIZONTAL,}

    actions = [
        '_action_make_moderated',
        '_action_set_queue',
        '_action_active_now',
        '_action_active_queue_8',
        '_action_active_queue_24',
    ]

    def cls_ok(self, obj):
        return bool(obj.cls_check)

    cls_ok.boolean = True
    cls_ok.short_description = 'Оценка (авто)'

    def _action_make_moderated(self, request, queryset):
        try:
            item = queryset.latest('pk')
            _start_week, _end_week = get_start_end_of_week(
                item.related_to_date)
            issue = Issue.objects.filter(date_from=_start_week,
                                         date_to=_end_week)
            assert len(issue) == 1
            issue.update(last_item=item.pk)
        except Exception:
            raise

    _action_make_moderated.short_description = 'Отмодерирован'

    def _action_active_now(self, request, queryset):
        queryset.update(
            activated_at=datetime.now(),
            status='active',
        )

    _action_active_now.short_description = 'Активировать сейчас'

    def _action_active_queue_n_hourn(self, period_len, queryset):
        try:
            items = queryset.filter(status='queue').order_by('pk')
            assert items.count() > 0
            _interval = int(period_len / items.count() * 60)  # in minutes

            _time = datetime.now()
            for x in items:
                x.activated_at = _time
                x.status = 'active'
                x.save()
                _time += timedelta(minutes=_interval)
        except Exception:
            pass

    def _action_active_queue_24(self, request, queryset):
        self._action_active_queue_n_hourn(24, queryset)

    _action_active_queue_24.short_description = 'Активировать по очереди(24 часа)'

    def _action_active_queue_8(self, request, queryset):
        self._action_active_queue_n_hourn(8, queryset)

    _action_active_queue_8.short_description = 'Активировать по очереди(8 часов)'

    def _action_set_queue(self, request, queryset):
        queryset.update(status='queue')

    _action_set_queue.short_description = 'В очередь'

    def get_queryset(self, request):

        # todo
        # потом переписать на логику:
        # ищем связку выпусков
        # неактивный, а перед ним активный
        # если такая есть, то публикуем новости у которых время в периоде
        # неактивного
        # если нету, то  отдаем все

        # сейчас логика такая:
        # берем выпуск за текущую неделю
        # если перед ним активный, то показываем новость за текущую неделю
        # если нет, то все новости показываем
        try:
            start_week, end_week = get_start_end_of_week(datetime.now().date())
            before_issue = Issue.objects.filter(
                date_to=end_week - timedelta(days=7))
            assert len(before_issue) == 1
            if before_issue[0].status == 'active':
                current_issue = Issue.objects.filter(date_to=end_week,
                                                     date_from=start_week)
                assert len(current_issue) == 1
                current_issue = current_issue[0]
            else:
                current_issue = before_issue[0]

            result = self.model.objects.filter(
                related_to_date__range=[current_issue.date_from,
                                        current_issue.date_to])

            if current_issue.last_item is not None:
                result = result.filter(pk__gt=current_issue.last_item, )
        except AssertionError:
            result = super(ItemModeratorAdmin, self).get_queryset(request)
        return result

    external_link = lambda s, obj: _external_link(obj)
    external_link.allow_tags = True
    external_link.short_description = 'Ссылка'

    external_link_edit = lambda s, obj: link_html(obj)
    external_link_edit.allow_tags = True
    external_link_edit.short_description = 'Ссылка'

    def save_model(self, request, obj, form, change):
        _save_item_model(request, obj, form, change)

        super(ItemModeratorAdmin, self).save_model(request, obj, form, change)


admin.site.register(ItemModerator, ItemModeratorAdmin)


class ItemDailyModerator(Item):
    class Meta:
        proxy = True
        verbose_name_plural = 'Новости (разметка дневного дайджеста)'


class ItemDailyModeratorAdmin(admin.ModelAdmin):
    # filter_horizontal = ('tags',)
    list_editable = ('is_editors_choice',)
    list_display = ('title', 'status', 'is_editors_choice', 'external_link',
                    'activated_at', 'cls_ok')

    external_link = lambda s, obj: _external_link(obj)
    external_link.allow_tags = True
    external_link.short_description = 'Ссылка'

    def cls_ok(self, obj):
        return obj.cls_check

    cls_ok.boolean = True
    cls_ok.short_description = 'Оценка (авто)'

    def get_queryset(self, request):
        try:

            today = datetime.utcnow().date()
            yeasterday = today - timedelta(days=2)

            result = self.model.objects.filter(
                related_to_date__range=[yeasterday,
                                        today],
                status='active').order_by('-pk')
        except AssertionError:
            result = super(ItemDailyModeratorAdmin, self).get_queryset(request)
        return result

    def save_model(self, request, obj, form, change):
        _save_item_model(request, obj, form, change)
        super(ItemDailyModeratorAdmin, self).save_model(request, obj, form,
                                                        change)


admin.site.register(ItemDailyModerator, ItemDailyModeratorAdmin)


class ItemCls(Item):
    class Meta:
        proxy = True
        verbose_name_plural = 'Новости (классификатор)'


class ItemClsAdmin(admin.ModelAdmin):
    # filter_horizontal = ('tags',)
    list_filter = (
        'status',
        'issue',
        'section',
        'resource',
    )
    search_fields = ('title', 'description', 'link')
    list_display = ('title', 'external_link', 'status_ok',
                    'cls_ok')

    external_link = lambda s, obj: _external_link(obj)
    external_link.allow_tags = True
    external_link.short_description = 'Ссылка'

    def status_ok(self, obj):
        return obj.status == 'active'

    status_ok.boolean = True
    status_ok.short_description = 'Модератор'

    def cls_ok(self, obj):
        return obj.cls_check

    cls_ok.boolean = True
    cls_ok.short_description = 'Классификатор'

    def get_queryset(self, request):
        try:
            return super(ItemClsAdmin, self).get_queryset(request).filter(
                pk__lte=Issue.objects.all().first().last_item)
        except ValueError as e:
            print(e)
            return super(ItemClsAdmin, self).get_queryset(request)


admin.site.register(ItemCls, ItemClsAdmin)


class ItemClsCheckAdmin(admin.ModelAdmin):
    fields = (
        'item',
        'score',
        'last_check',
    )
    readonly_fields = (
        'last_check',
    )
    list_display = (
        'item',
        'last_check',
        'score',
    )

    list_filter = (
        'score',
        'last_check',
    )

    actions = [
        'update_check',
    ]

    def update_check(self, request, queryset):
        for obj in queryset.all():
            obj.check_cls(force=True)

    update_check.short_description = 'Перепроверить классификатором'


admin.site.register(ItemClsCheck, ItemClsCheckAdmin)

if likes_enable():
    from secretballot.models import Vote

    admin.site.register(Vote)
