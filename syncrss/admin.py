from django.contrib import admin
from syncrss.models import RawItem, ResourceRSS

class RawItemAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields':['title']}),
        ('Date information', {'fields':['related_to_date'], 'classes': ['collapse']}),
    ]

    list_display = ('title', 'link', 'related_to_date')
    list_filter = ('title','related_to_date')
    search_fields = ['title']
admin.site.register(RawItem, RawItemAdmin)


class ResourceRSSAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'sync_date')
    list_filter = ('status', 'sync_date',)
    search_fields = ['title']
admin.site.register(ResourceRSS, ResourceRSSAdmin)
