from django.urls import path

from .views import AddNews, IssuesList, IssueView, ItemView, NewsList, get_items_json

app_name = 'digest'
urlpatterns = [
    path('view/<int:pk>/', ItemView.as_view(), name='item'),
    path('issues/', IssuesList.as_view(), name='issues'),
    path('issue/<int:pk>/', IssueView.as_view(), name='issue_view'),
    path('add/', AddNews.as_view(), name='addnews'),
    path('feed/', NewsList.as_view(), name='feed'),
    path('api/items/<int:year>/<int:month>/<int:day>/',
        get_items_json),
]
