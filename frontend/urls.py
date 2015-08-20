from django.conf.urls import patterns, url

from frontend.views import AddNews, Index, IssuesList, \
    IssueView, ItemView, NewsList, Sitemap

from .feeds import AllEntriesFeed, IssuesFeed, ItemArticleFeed, \
    ItemBookDocFeed, ItemEventFeed, ItemNewsFeed, \
    ItemPackagesFeed, ItemRecommendFeed, ItemReleaseFeed, \
    ItemVideoFeed, RussianEntriesFeed, TwitterEntriesFeed

urlpatterns = patterns(
    '', url(r'^view/(?P<pk>[0-9]+)/$', ItemView.as_view(),
            name='item'), url(r'^add/$', AddNews.as_view(),
                              name='addnews'),
    url(r'^feed/$', NewsList.as_view(),
        name='feed'), url(r'^rss/$', AllEntriesFeed(),
                          name='rss'), url(r'^rss/direct/$', AllEntriesFeed(),
                                           name='rss_direct'),
    url(r'^rss/twitter/$', TwitterEntriesFeed(),
        name='rss_twitter'), url(r'^rss/ru/$', RussianEntriesFeed(),
                                 name='russian_rss'),
    url(r'^rss/issues/$', IssuesFeed(),
        name='issues_rss'),  # hindi
    # solution
    url(r'^rss/video/$', ItemVideoFeed(),
        name='video_rss'
        ), url(r'^rss/recommend/$', ItemRecommendFeed(),
               name='recommend_rss'), url(r'^rss/news/$', ItemNewsFeed(),
                                          name='news_rss'),
    url(r'^rss/bookdoc/$', ItemBookDocFeed(),
        name='book_doc_rss'), url(r'^rss/event/$', ItemEventFeed(),
                                  name='event_rss'),
    url(r'^rss/article/$', ItemArticleFeed(),
        name='article_rss'), url(r'^rss/release/$', ItemReleaseFeed(),
                                 name='release_rss'),
    url(r'^rss/packages/$', ItemPackagesFeed(),
        name='packages_rss'), url(r'^issues/$', IssuesList.as_view(),
                                  name='issues'),
    url(r'^issue/(?P<pk>[0-9]+)/$', IssueView.as_view(),
        name='issue_view'), url(r'^sitemap\.xml$', Sitemap.as_view(),
                                name='sitemap'), url(r'^$', Index.as_view(),
                                                     name='home'), )
