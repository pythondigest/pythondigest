# -*- coding: utf-8 -*-
import django.views.static
from controlcenter.views import controlcenter
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from conf.utils import likes_enable
from digest.urls import urlpatterns as digest_url
from frontend.urls import urlpatterns as frontend_url

admin.autodiscover()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/dashboard/', controlcenter.urls),
    url(r'^media/(?P<path>.*)$', django.views.static.serve,
        {'document_root': settings.MEDIA_ROOT}),
    url(r'', include(frontend_url, namespace='frontend')),
    url(r'', include(digest_url, namespace='digest')),

    url(r'^taggit_autosuggest/', include('taggit_autosuggest.urls')),
    # url(r'^account/', include('account.urls')),
    # url(r'', include('social.apps.django_app.urls', namespace='social'))
]

if 'landings' in settings.INSTALLED_APPS:
    from landings.urls import urlpatterns as landings_url

    urlpatterns.append(url(r'', include(landings_url, namespace='landings')))

if 'jobs' in settings.INSTALLED_APPS:
    from jobs.urls import urlpatterns as jobs_url

    urlpatterns.append(url(r'', include(jobs_url, namespace='jobs')))

if likes_enable():
    from likes.urls import urlpatterns as like_urls

    urlpatterns.append(url(r'^likes/', include(like_urls)))

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns.append(url(r'^rosetta/', include('rosetta.urls')))

if 'debug_toolbar' in settings.INSTALLED_APPS and settings.DEBUG:
    import debug_toolbar

    urlpatterns.append(url(r'^__debug__/', include(debug_toolbar.urls)))

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()