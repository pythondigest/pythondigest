# -*- coding: utf-8 -*-

from django.contrib import admin
from django.db import models
from django import forms
from django.core.urlresolvers import reverse
from digest.models import Issue, IssueHabr, Section, Item, Resource, AutoImportResource

from django.contrib.sites.models import Site
admin.site.unregister(Site)


class IssueAdmin(admin.ModelAdmin):
    list_display = ('title', 'frontend_link', 'habr_link')

    def frontend_link(self,obj):
        lnk = reverse('frontend:issue_view', kwargs={'pk': obj.pk})
        return u'<a target="_blank" href="%s">%s</a>' % (lnk, lnk)
    frontend_link.allow_tags = True
    frontend_link.short_description = u"Просмотр"

    def habr_link(self,obj):
        lnk = reverse('frontend:habr_issue_view', kwargs={'pk': obj.pk})
        return u'<a target="_blank" href="%s">%s</a>' % (lnk, lnk)
    habr_link.allow_tags = True
    habr_link.short_description = u"Хабраверстка"
admin.site.register(Issue, IssueAdmin)


class IssueHabrAdmin(admin.ModelAdmin):
    list_display = ('title', 'habr_link')

    def habr_link(self,obj):
        lnk = reverse('frontend:habr_issue_view', kwargs={'pk': obj.pk})
        return u'<a target="_blank" href="%s">%s</a>' % (lnk, lnk)
    habr_link.allow_tags = True
    habr_link.short_description = u"Хабраверстка"
admin.site.register(IssueHabr, IssueHabrAdmin)


class SectionAdmin(admin.ModelAdmin):
    pass
admin.site.register(Section, SectionAdmin)


class ItemAdmin(admin.ModelAdmin):
    list_filter = ('status', 'issue', 'is_editors_choice', 'user')
    search_fields = ('title', 'description', 'link', 'resource__title')
    list_display = ('title', 'status', 'is_editors_choice', 'external_link', 'resource', 'issue', 'related_to_date')
    list_editable = ('is_editors_choice',)
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
    list_display = ('name', 'link_html', 'type_res', 'resource', 'incl', 'excl', 'in_edit')
    formfield_overrides = {
            models.TextField: {'widget': forms.Textarea(attrs={'cols': 45, 'rows': 1 })},
        }
    def link_html(self,obj):
        return u'<a target="_blank" href="%s">%s</a>' % (obj.link, obj.link)
    link_html.allow_tags = True
    link_html.short_description = u"Ссылка"
admin.site.register(AutoImportResource, AutoImportResourceAdmin)
