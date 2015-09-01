# -*- coding: utf-8 -*-
from django.contrib import admin

from digest.admin import link_html
from jobs.models import JobFeed, JobItem, AcceptedList, RejectedList


class JobFeedAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'link_html',
        'in_edit',
    )

    link_html = lambda s, obj: link_html(obj)
    link_html.allow_tags = True
    link_html.short_description = u"Ссылка"

class RejectedListAdmin(admin.ModelAdmin):
    pass

class AcceptedListAdmin(admin.ModelAdmin):
    pass

class JobItemAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'link',
        'url_api',
        'url_logo',
        'place',
        'salary_from',
        'employer_name',
        'salary_currency',
    )

    link_html = lambda s, obj: link_html(obj)
    link_html.allow_tags = True
    link_html.short_description = u"Ссылка"


admin.site.register(JobItem, JobItemAdmin)
admin.site.register(JobFeed, JobFeedAdmin)
admin.site.register(RejectedList, RejectedListAdmin)
admin.site.register(AcceptedList, AcceptedListAdmin)