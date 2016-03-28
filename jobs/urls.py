# -*- encoding: utf-8 -*-
from django.conf.urls import url

from jobs.views import JobList

app_name = 'jobs'
urlpatterns = [
    url(r'^jobs/$', JobList.as_view(), name='job_feed'),
]
