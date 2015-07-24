# -*- coding: utf-8 -*-
from datetime import datetime

from django.contrib import admin
from django.db import models
from django import forms
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from goslate import Goslate
from django.core.cache import cache

from digest.models import Issue, Section, Item, Resource, AutoImportResource
admin.site.unregister(Site)


class IssueAdmin(admin.ModelAdmin):
    list_display = ('title', 'frontend_link',)

    def frontend_link(self,obj):
        lnk = reverse('frontend:issue_view', kwargs={'pk': obj.pk})
        return u'<a target="_blank" href="%s">%s</a>' % (lnk, lnk)
    frontend_link.allow_tags = True
    frontend_link.short_description = u"Просмотр"

admin.site.register(Issue, IssueAdmin)


class SectionAdmin(admin.ModelAdmin):
    pass
admin.site.register(Section, SectionAdmin)


class ItemAdmin(admin.ModelAdmin):
    list_filter = ('status', 'issue', 'section', 'is_editors_choice', 'user', 'related_to_date')
    search_fields = ('title', 'description', 'link', 'resource__title')
    list_display = (
        '_title', 'status', 'external_link', 'is_editors_choice',
        'related_to_date')

    list_editable = ('is_editors_choice',)
    exclude = ('modified_at',),
    radio_fields = {
        'language': admin.HORIZONTAL,
        'status': admin.HORIZONTAL,
    }

    def _title(self, obj):
        if obj.id:
            opts = self.model._meta
            link = "<a href='%s' target='_blank'>%s</a>" % (reverse(
                'admin:%s_%s_change' % (
                    opts.app_label, opts.object_name.lower()),
                args=[obj.id]
            ), obj.title)

            cache_key = '_pydigest_%s_title' % obj.id
            translate = cache.get(cache_key)
            if translate is None:
                translate = Goslate().translate(obj.title, 'ru')
                cache.set(cache_key, translate)
            if translate != obj.title:
                result = u"%s <br> Перевод: %s" % (link, translate)
            else:
                result = link
            return result
        else:
            return u"(save to edit details)"

    def external_link(self, obj):
        lnk = obj.link
        ret = u'<a target="_blank" href="%s">Ссылка&nbsp;&gt;&gt;&gt;</a>' % lnk
        username = obj.user.username if obj.user else u'Гость'
        ret = u'%s<br>Добавил: %s' % (ret, username)
        return ret

    _title.short_description = u"Title"
    _title.allow_tags = True
    external_link.allow_tags = True
    external_link.short_description = u"Ссылка"

    def save_model(self, request, obj, form, change):
        prev_status = False
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
        else:
            old_obj = Item.objects.get(pk=obj.pk)
            prev_status = old_obj.status

        # Обновление времени модификации при смене статуса на активный
        new_status = form.cleaned_data.get('status')
        if not prev_status == 'active' and new_status == 'active':
            obj.modified_at = datetime.now()

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
    list_display = ('name', 'link_html', 'type_res', 'resource', 'incl', 'excl', 'in_edit', 'language')
    formfield_overrides = {
            models.TextField: {'widget': forms.Textarea(attrs={'cols': 45, 'rows': 1 })},
        }
    def link_html(self,obj):
        return u'<a target="_blank" href="%s">%s</a>' % (obj.link, obj.link)
    link_html.allow_tags = True
    link_html.short_description = u"Ссылка"
admin.site.register(AutoImportResource, AutoImportResourceAdmin)
