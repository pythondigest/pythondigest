from django.conf.urls import url

from frontend.views import IndexView, Sitemap, FriendsView
from .feeds import AllEntriesFeed, IssuesFeed, ItemArticleFeed, \
    ItemBookDocFeed, ItemEventFeed, ItemNewsFeed, \
    ItemPackagesFeed, ItemRecommendFeed, ItemReleaseFeed, \
    ItemVideoFeed, RussianEntriesFeed, TwitterEntriesFeed, ItemAuthorsFeed, RawEntriesFeed

app_name = 'frontend'
urlpatterns = [
    url(r'^rss/$', AllEntriesFeed(), name='rss'),
    url(r'^rss/raw$', RawEntriesFeed(), name='rss_raw'),
    url(r'^rss/direct/$', AllEntriesFeed(), name='rss_direct'),
    url(r'^rss/twitter/$', TwitterEntriesFeed(), name='rss_twitter'),
    url(r'^rss/ru/$', RussianEntriesFeed(), name='russian_rss'),
    url(r'^rss/issues/$', IssuesFeed(), name='issues_rss'),  # hindi
    # solution
    url(r'^rss/video/$', ItemVideoFeed(), name='video_rss'),
    url(r'^rss/recommend/$', ItemRecommendFeed(), name='recommend_rss'),
    url(r'^rss/news/$', ItemNewsFeed(), name='news_rss'),
    url(r'^rss/bookdoc/$', ItemBookDocFeed(), name='book_doc_rss'),
    url(r'^rss/event/$', ItemEventFeed(), name='event_rss'),
    url(r'^rss/article/$', ItemArticleFeed(), name='article_rss'),
    url(r'^rss/authors/$', ItemAuthorsFeed(), name='authors_rss'),
    url(r'^rss/release/$', ItemReleaseFeed(), name='release_rss'),
    url(r'^rss/packages/$', ItemPackagesFeed(), name='packages_rss'),

    url(r'^sitemap\.xml$', Sitemap.as_view(), name='sitemap'),
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^friends/$', FriendsView, name='friends'),
]
