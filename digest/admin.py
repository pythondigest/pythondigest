# -*- coding: utf-8 -*-

from django.contrib import admin
from django import forms
from digest.models import Issue, Section, Item, Resource

class IssueAdmin(admin.ModelAdmin):
    exclude = ('version',)
    pass
admin.site.register(Issue, IssueAdmin)

class SectionAdmin(admin.ModelAdmin):
    exclude = ('version',)
    pass
admin.site.register(Section, SectionAdmin)


class ItemAdmin(admin.ModelAdmin):
    list_filter = ('status', 'issue',)
    list_display = ('title', 'status', 'issue', 'related_to_date')
    radio_fields = {'language': admin.HORIZONTAL}
    exclude = ('version',)
admin.site.register(Item, ItemAdmin)

class ResourceAdmin(admin.ModelAdmin):
    exclude = ('version',)
    pass
admin.site.register(Resource, ResourceAdmin)
