# -*- coding: utf-8 -*-
from django.contrib import admin
from syncrss.models import RawItem, ResourceRSS
from digest.models import Item

class ResourceRSSAdmin(admin.ModelAdmin):
    list_display = ('title', 'language', 'status', 'sync_date')
    list_filter = ('language', 'status', 'sync_date',)
    search_fields = ['title']
admin.site.register(ResourceRSS, ResourceRSSAdmin)


def make_published(modeladmin, request, queryset):
    for news in queryset:
        # soooo... ugly
        obj = Item(title=news.title, \
            description=news.description, \
            link=news.link,status=news.status, \
            related_to_date=news.related_to_date, \
            language=news.language, \
            version=news.version)
        obj.save()
    # закоментить если не нужно чтобы новости удалялись
    queryset.delete()

make_published.short_description = "Перенести выделенные новости в ленту"

class RawItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'link', 'related_to_date', 'status')
    list_filter = ('resource_rss', 'related_to_date', 'status')
    search_fields = ['title']
    actions = [make_published]
admin.site.register(RawItem, RawItemAdmin)
