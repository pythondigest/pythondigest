# -*- coding: utf-8 -*-
import django.views.static
from controlcenter.views import controlcenter
from django.conf import settings
from django.conf.urls import include, patterns, url
from django.contrib import admin
from likes.urls import urlpatterns as like_urls

from digest.urls import urlpatterns as digest_url
from frontend.urls import urlpatterns as frontend_url
from jobs.urls import urlpatterns as jobs_url

admin.autodiscover()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/dashboard/', controlcenter.urls),
    url(r'^media/(?P<path>.*)$', django.views.static.serve, {'document_root': settings.MEDIA_ROOT}),
    url(r'', include(frontend_url, namespace='frontend')),
    url(r'', include(digest_url, namespace='digest')),
    url(r'', include(jobs_url, namespace='jobs')),
    url(r'^likes/', include(like_urls)),
    # url(r"^account/", include('account.urls')),
    # url(r'', include('social.apps.django_app.urls', namespace='social'))
]

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += patterns('', url(r'^rosetta/', include('rosetta.urls')), )

if 'debug_toolbar' in settings.INSTALLED_APPS and settings.DEBUG:
    import debug_toolbar

    urlpatterns += patterns('', url(r'^__debug__/', include(debug_toolbar.urls)), )
