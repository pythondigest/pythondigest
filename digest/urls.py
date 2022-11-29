from django.conf.urls import url
from django.urls import path

from .views import (AddNews, IssuesList, IssueView, ItemView, NewsList,
                    get_items_json)

app_name = 'digest'
urlpatterns = [
    path('view/(?P<pk>[0-9]+)/$', ItemView.as_view(), name='item'),
    path('issues/$', IssuesList.as_view(), name='issues'),
    path('issue/(?P<pk>[0-9]+)/$', IssueView.as_view(), name='issue_view'),
    path('add/$', AddNews.as_view(), name='addnews'),
    path('feed/$', NewsList.as_view(), name='feed'),
    path('api/items/(?P<year>[0-9]+)/(?P<month>[0-9]+)/(?P<day>[0-9]+)/$',
        get_items_json),
]
