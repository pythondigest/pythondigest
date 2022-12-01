# -*- encoding: utf-8 -*-
from django.urls import path

from jobs.views import JobList

app_name = 'jobs'
urlpatterns = [
    path('jobs/', JobList.as_view(), name='job_feed'),
]
