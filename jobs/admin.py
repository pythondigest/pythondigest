# -*- coding: utf-8 -*-
from django.contrib import admin

from digest.admin import link_html
from jobs.models import JobFeed


class JobFeedAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'link_html',
        'incl',
        'excl',
        'in_edit',
    )

    link_html = lambda s, obj: link_html(obj)
    link_html.allow_tags = True
    link_html.short_description = u"Ссылка"


admin.site.register(JobFeed, JobFeedAdmin)
