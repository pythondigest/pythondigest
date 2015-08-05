# coding=utf-8

from django.contrib import admin

from frontend.models import EditorMaterial, Tip


class EditorMaterialAdmin(admin.ModelAdmin):
    list_display = ('title', 'link_html', 'status', 'section', 'user', 'created_at')
    search_fields = ('title', 'announce', 'contents')
    list_filter = ('status', 'user', 'section')
    prepopulated_fields = {'slug': ('title',), }

    radio_fields = {
        'section': admin.HORIZONTAL,
        'status': admin.HORIZONTAL,
    }

    def link_html(self, obj):
        return '<a href="%s">читать</a>' % obj.link
    link_html.allow_tags = True
    link_html.short_description = u'Ссылка'

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.user = request.user
        super(EditorMaterialAdmin, self).save_model(request, obj, form, change)
admin.site.register(EditorMaterial, EditorMaterialAdmin)


class TipAdmin(admin.ModelAdmin):
    list_display = (
        'text',
        'active'
    )

    list_editable = (
        'active',
    )


admin.site.register(Tip, TipAdmin)
