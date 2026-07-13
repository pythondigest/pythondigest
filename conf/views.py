from django.http import HttpResponse
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_GET


@never_cache
@require_GET
def ping(request):
    return HttpResponse("pong", content_type="text/plain")
