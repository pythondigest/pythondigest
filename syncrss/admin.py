from django.contrib import admin
from syncrss.models import RawItem, ResourceRSS

class ResourceRSSAdmin(admin.ModelAdmin):
    list_display = ('title', 'language', 'status', 'sync_date')
    list_filter = ('language', 'status', 'sync_date',)
    search_fields = ['title']
admin.site.register(ResourceRSS, ResourceRSSAdmin)


class RawItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'language', 'resource_rss', 'status', 'section', 'link', 'related_to_date')
    list_filter = ('title', 'language', 'resource_rss', 'related_to_date')
    search_fields = ['title']
admin.site.register(RawItem, RawItemAdmin)
