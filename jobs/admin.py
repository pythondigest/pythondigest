# -*- coding: utf-8 -*-
from django.contrib import admin

from digest.admin import link_html
from jobs.models import JobFeed, JobItem, AcceptedList, RejectedList
from jobs.utils import format_currency


class JobFeedAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'link_html',
        'is_activated',
        'in_edit',
    )

    list_editable = [
        'is_activated',
    ]

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
        'link_html',
        'published_at',
        'src_place_name',
        '_salary_text',
    )

    link_html = lambda s, obj: link_html(obj)
    link_html.allow_tags = True
    link_html.short_description = u"Ссылка"

    def _salary_text(self, obj):
        result = ''
        result += ' от %s' % format_currency(obj.salary_from) if obj.salary_from else ''
        result += ' до %s' % format_currency(obj.salary_till) if obj.salary_till else ''
        result += ' ' + obj.salary_currency if obj.salary_currency else ''
        return result

    _salary_text.short_description = u"Зарплата"

admin.site.register(JobItem, JobItemAdmin)
admin.site.register(JobFeed, JobFeedAdmin)
admin.site.register(RejectedList, RejectedListAdmin)
admin.site.register(AcceptedList, AcceptedListAdmin)