# -*- coding: utf-8 -*-

from django.contrib import admin
from django import forms
from django.core.urlresolvers import reverse
from digest.models import Issue, Section, Item, Resource


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


class SectionAdmin(admin.ModelAdmin):
    pass
admin.site.register(Section, SectionAdmin)


class ItemAdmin(admin.ModelAdmin):
    list_filter = ('status', 'issue',)
    search_fields = ('title', 'description', 'link', 'resource__title')
    list_display = ('title', 'status', 'issue', 'related_to_date')
    radio_fields = {'language': admin.HORIZONTAL}
admin.site.register(Item, ItemAdmin)


class ResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'link_html')

    def link_html(self,obj):
        return u'<a target="_blank" href="%s">%s</a>' % (obj.link, obj.link)
    link_html.allow_tags = True
    link_html.short_description = u"Ссылка"
admin.site.register(Resource, ResourceAdmin)
