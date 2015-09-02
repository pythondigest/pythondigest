# -*- encoding: utf-8 -*-
from django.conf.urls import patterns, url

from jobs.views import JobList

urlpatterns = patterns(
    '',
    url(r'^jobs/$', JobList.as_view(), name='job_feed'),
)
