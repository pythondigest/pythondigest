from django.conf.urls import patterns, include, url

from frontend.views import (
    Index,
    IssuesList,
    IssueView
)

urlpatterns = patterns('frontend.urls',
    url(r'^issues/$', IssuesList.as_view(), name='issues'),
    url(r'^issue/(?P<pk>[0-9]+)/$', IssueView.as_view(), name='issue_view'),
    url(r'^$', Index.as_view(), name='home'),
)

