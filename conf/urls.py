from django.conf import settings
from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.contrib.sitemaps import Sitemap
from digest.models import Issue, Item

admin.autodiscover()

class IssueSitemap(Sitemap):

    changefreq = "never"
    priority = 0.5
    i18n = True

    def items(self):
        return Issue.objects.filter(status='active')

    def lastmod(self, obj):
        return obj.published_at



sitemaps = {
    'issue': IssueSitemap,
}

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    url(r'', include('frontend.urls', namespace='frontend')),
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap')
)
