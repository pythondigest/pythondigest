from django.contrib import admin
from subscribe.models import  Subscribers


class SubscribersAdmin(admin.ModelAdmin):

    list_display = ('useremail',
                    'subscribe',
                    'id_subscriber',
                    'subscriber_add')


admin.site.register(Subscribers, SubscribersAdmin)
