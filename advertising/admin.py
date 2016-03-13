from django.contrib import admin

from .models import AdPage, AdType, AdAlign, Advertising

admin.site.register(AdAlign)
admin.site.register(AdPage)
admin.site.register(AdType)
admin.site.register(Advertising)
