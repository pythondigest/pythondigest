# -*- coding: utf-8 -*-
from datetime import datetime

from django.contrib import admin
from django.db import models
from django import forms
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site

from digest.models import Issue, Section, Item, Resource, AutoImportResource, \
    ParsingRules, Tag
admin.site.unregister(Site)


class IssueAdmin(admin.ModelAdmin):
    list_display = ('title', 'frontend_link',)

    def frontend_link(self,obj):
        lnk = reverse('frontend:issue_view', kwargs={'pk': obj.pk})
        return u'<a target="_blank" href="%s">%s</a>' % (lnk, lnk)
    frontend_link.allow_tags = True
    frontend_link.short_description = u"Просмотр"

admin.site.register(Issue, IssueAdmin)


class SectionAdmin(admin.ModelAdmin):
    pass
admin.site.register(Section, SectionAdmin)


class ParsingRulesAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'is_activated',
        'if_element',
        '_get_if_action',
        'then_element',
        '_get_then_action',
    )

    list_filter = (
        'is_activated',
        'if_element',
        'if_action',
        'then_element',
        'then_action',
    )

    list_editable = (
        'is_activated',
    )

    search_fields = (
        'is_activated',
        'name',
        'if_value',
        'then_value',
    )

    def _get_if_action(self, obj):
        return u"{}: <i>{}</i>".format(obj.get_if_action_display(), obj.if_value)

    _get_if_action.allow_tags = True
    _get_if_action.short_description = u"Условие"

    def _get_then_action(self, obj):
        return u"{}: <i>{}</i>".format(obj.get_then_action_display(), obj.then_value)

    _get_then_action.allow_tags = True
    _get_then_action.short_description = u"Действие"

admin.site.register(ParsingRules, ParsingRulesAdmin)


class TagAdmin(admin.ModelAdmin):
    pass


admin.site.register(Tag, TagAdmin)


class ItemAdmin(admin.ModelAdmin):
    fields = (
        'section',
        'title',
        'is_editors_choice',
        'description',
        'issue',
        'link',
        'status',
        'language',
        'related_to_date',
        'tags',
    )
    filter_horizontal = ('tags',)
    list_filter = ('status', 'issue', 'section', 'is_editors_choice', 'user', 'related_to_date')
    search_fields = ('title', 'description', 'link', 'resource__title')
    list_display = (
        'title', 'status',
        'external_link',
        'related_to_date',
        'is_editors_choice',
    )

    list_editable = ('is_editors_choice',)
    exclude = ('modified_at',),
    radio_fields = {
        'language': admin.HORIZONTAL,
        'status': admin.HORIZONTAL,
    }

    def external_link(self, obj):
        lnk = obj.link
        ret = u'<a target="_blank" href="%s">Ссылка&nbsp;&gt;&gt;&gt;</a>' % lnk
        username = obj.user.username if obj.user else u'Гость'
        ret = u'%s<br>Добавил: %s' % (ret, username)
        return ret

    external_link.allow_tags = True
    external_link.short_description = u"Ссылка"

    def save_model(self, request, obj, form, change):
        prev_status = False
        if not obj.pk:
            obj.user = request.user
            if not obj.issue:
                la = lna = False
                qs = Issue.objects
                try:
                    # последний активный
                    la = qs.filter(status='active').order_by('-pk')[0:1].get()
                    # последний неактивный
                    lna = qs.filter(pk__gt=la.pk).order_by('pk')[0:1].get()
                except Issue.DoesNotExist:
                    pass

                if la or lna:
                    obj.issue = lna or la
        else:
            old_obj = Item.objects.get(pk=obj.pk)
            prev_status = old_obj.status

        # Обновление времени модификации при смене статуса на активный
        new_status = form.cleaned_data.get('status')
        if not prev_status == 'active' and new_status == 'active':
            obj.modified_at = datetime.now()

        super(ItemAdmin, self).save_model(request, obj, form, change)
admin.site.register(Item, ItemAdmin)


class ResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'link_html')

    def link_html(self,obj):
        return u'<a target="_blank" href="%s">%s</a>' % (obj.link, obj.link)
    link_html.allow_tags = True
    link_html.short_description = u"Ссылка"
admin.site.register(Resource, ResourceAdmin)


class AutoImportResourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'link_html', 'type_res', 'resource', 'incl', 'excl', 'in_edit', 'language')
    formfield_overrides = {
            models.TextField: {'widget': forms.Textarea(attrs={'cols': 45, 'rows': 1 })},
    }

    def link_html(self,obj):
        return u'<a target="_blank" href="%s">%s</a>' % (obj.link, obj.link)
    link_html.allow_tags = True
    link_html.short_description = u"Ссылка"


admin.site.register(AutoImportResource, AutoImportResourceAdmin)
