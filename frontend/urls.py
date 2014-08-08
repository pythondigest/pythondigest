from feeds import LatestEntriesFeed, IssuesFeed
from django.conf.urls import patterns, url

from frontend.views import (
    Index,
    IssuesList,
    IssueView,
    HabrView,
    NewsList,
    AddNews,
)

urlpatterns = patterns(
    'frontend.urls',
    url(r'^add/', AddNews.as_view(), name='addnews'),
    url(r'^feed/$', NewsList.as_view(), name='feed'),
    url(r'^rss/$', LatestEntriesFeed(), name='rss'),
    url(r'^rss/issues/$', IssuesFeed(), name='issues_rss'),
    url(r'^issues/$', IssuesList.as_view(), name='issues'),
    url(r'^issue/(?P<pk>[0-9]+)/$', IssueView.as_view(), name='issue_view'),
    url(r'^habr/(?P<pk>[0-9]+)/$', HabrView.as_view(), name='habr_issue_view'),
    url(r'^$', Index.as_view(), name='home'),
)

