from django.contrib import admin
from syncrss.models import RawItem, ResourceRSS

class RawItemAdmin(admin.ModelAdmin):
    pass
admin.site.register(RawItem, RawItemAdmin)


class ResourceRSSAdmin(admin.ModelAdmin):
    pass
admin.site.register(ResourceRSS, ResourceRSSAdmin)
