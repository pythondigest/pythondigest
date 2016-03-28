from django.conf.urls import url

from .views import IssuesList, \
    IssueView, ItemView, AddNews, NewsList


app_name = 'digest'
urlpatterns = [
    url(r'^view/(?P<pk>[0-9]+)/$', ItemView.as_view(), name='item'),
    url(r'^issues/$', IssuesList.as_view(), name='issues'),
    url(r'^issue/(?P<pk>[0-9]+)/$', IssueView.as_view(), name='issue_view'),
    url(r'^add/$', AddNews.as_view(), name='addnews'),
    url(r'^feed/$', NewsList.as_view(), name='feed'),
]
