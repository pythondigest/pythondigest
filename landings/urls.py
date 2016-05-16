# -*- encoding: utf-8 -*-

from django.conf.urls import url

from .views import DjangoPage

urlpatterns = [

    url(r'^django$', DjangoPage.as_view(), name='django'),
]
