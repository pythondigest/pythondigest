# -*- coding: utf-8 -*-

from django.contrib import admin
from digest.models import Issue, Section, Item, Resource

class IssueAdmin(admin.ModelAdmin):
    pass
admin.site.register(Issue, IssueAdmin)

class SectionAdmin(admin.ModelAdmin):
    pass
admin.site.register(Section, SectionAdmin)

class ItemAdmin(admin.ModelAdmin):
    list_filter = ('status', 'issue',)
    list_display = ('title', 'status', 'issue', 'related_to_date')
admin.site.register(Item, ItemAdmin)

class ResourceAdmin(admin.ModelAdmin):
    pass
admin.site.register(Resource, ResourceAdmin)
