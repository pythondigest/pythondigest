# -*- coding: utf-8 -*-
import django.views.static
# from controlcenter.views import controlcenter
from django.conf import settings
from django.contrib import admin
from django.urls import include, path

from conf.utils import likes_enable
from digest.urls import urlpatterns as digest_url
from frontend.urls import urlpatterns as frontend_url

admin.autodiscover()

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('admin/dashboard/', controlcenter.urls),
    path('media/(?P<url>.*)$', django.views.static.serve,
        {'document_root': settings.MEDIA_ROOT}),
    path('', include((frontend_url, 'frontend'), namespace='frontend')),
    path('', include((digest_url, "digest"), namespace='digest')),

    path('taggit_autosuggest/', include('taggit_autosuggest.urls')),
    # path('account/', include('account.urls')),
    # path('', include('social_django.urls', namespace='social'))
]

if 'landings' in settings.INSTALLED_APPS:
    from landings.urls import urlpatterns as landings_url

    urlpatterns.append(path('', include((landings_url, "landings"), namespace='landings')))

if 'jobs' in settings.INSTALLED_APPS:
    from jobs.urls import urlpatterns as jobs_url

    urlpatterns.append(path('', include((jobs_url, "jobs"), namespace='jobs')))

if likes_enable():
    from likes.urls import urlpatterns as like_urls

    urlpatterns.append(path('likes/', include(like_urls)))

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns.append(path('rosetta/', include('rosetta.urls')))

if 'debug_toolbar' in settings.INSTALLED_APPS and settings.DEBUG:
    import debug_toolbar

    urlpatterns.append(path('__debug__/', include(debug_toolbar.urls)))
