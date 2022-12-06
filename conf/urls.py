from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path

from conf.utils import likes_enable
from digest.urls import urlpatterns as digest_url
from frontend.urls import urlpatterns as frontend_url

admin.autodiscover()

urlpatterns = [
    path("", include((frontend_url, "frontend"), namespace="frontend")),
    path("", include((digest_url, "digest"), namespace="digest")),
    path("admin/", admin.site.urls),
    path("taggit_autosuggest/", include("taggit_autosuggest.urls")),
    # path('account/', include('account.urls')),
    re_path(r"^\.well-known/", include("letsencrypt.urls")),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if "landings" in settings.INSTALLED_APPS:
    from landings.urls import urlpatterns as landings_url

    urlpatterns.append(
        path("", include((landings_url, "landings"), namespace="landings"))
    )

if "jobs" in settings.INSTALLED_APPS:
    from jobs.urls import urlpatterns as jobs_url

    urlpatterns.append(path("", include((jobs_url, "jobs"), namespace="jobs")))

if likes_enable():
    from likes.urls import urlpatterns as like_urls

    urlpatterns.append(path("likes/", include(like_urls)))

if settings.DEBUG:
    urlpatterns.append(path("__reload__/", include("django_browser_reload.urls")))

if "debug_toolbar" in settings.INSTALLED_APPS and settings.DEBUG:
    import debug_toolbar

    urlpatterns.append(path("__debug__/", include(debug_toolbar.urls)))
