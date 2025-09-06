from django.conf import settings
from django.http import HttpResponse
from django.urls import path

from frontend.views import FriendsView, IndexView, Sitemap

from .feeds import (
    AllEntriesFeed,
    IssuesFeed,
    ItemArticleFeed,
    ItemAuthorsFeed,
    ItemBookDocFeed,
    ItemEventFeed,
    ItemNewsFeed,
    ItemPackagesFeed,
    ItemRecommendFeed,
    ItemReleaseFeed,
    ItemVideoFeed,
    RawEntriesFeed,
    RussianEntriesFeed,
    TurboFeed,
    TwitterEntriesFeed,
)

feed = TurboFeed()
feed.configure_analytics_yandex(settings.YANDEX_METRIKA_ID)


def indexnow_key(request):
    return HttpResponse(settings.SEO_INDEXNOW_KEY)


app_name = "frontend"
urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    # SEO
    path(f"{settings.SEO_INDEXNOW_KEY}.txt", indexnow_key, name="indexnow-key"),
    # RSS
    path("rss/", AllEntriesFeed(), name="rss"),
    path("rss/raw", RawEntriesFeed(), name="rss_raw"),
    path("rss/direct/", AllEntriesFeed(), name="rss_direct"),
    path("rss/twitter/", TwitterEntriesFeed(), name="rss_twitter"),
    path("rss/ru/", RussianEntriesFeed(), name="russian_rss"),
    path("rss/issues/", IssuesFeed(), name="issues_rss"),  # hindi
    # solution
    path("rss/video/", ItemVideoFeed(), name="video_rss"),
    path("rss/recommend/", ItemRecommendFeed(), name="recommend_rss"),
    path("rss/news/", ItemNewsFeed(), name="news_rss"),
    path("rss/bookdoc/", ItemBookDocFeed(), name="book_doc_rss"),
    path("rss/event/", ItemEventFeed(), name="event_rss"),
    path("rss/article/", ItemArticleFeed(), name="article_rss"),
    path("rss/authors/", ItemAuthorsFeed(), name="authors_rss"),
    path("rss/release/", ItemReleaseFeed(), name="release_rss"),
    path("rss/packages/", ItemPackagesFeed(), name="packages_rss"),
    path("turbo/", feed),
    path("sitemap.xml", Sitemap.as_view(), name="sitemap"),
    path("friends/", FriendsView.as_view(), name="friends"),
]
