# -*- encoding: utf-8 -*-

from django.urls import path

from .views import DjangoPage

urlpatterns = [

    path('django$', DjangoPage.as_view(), name='django'),
]
