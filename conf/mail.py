from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse


def send_validation(strategy, backend, code):
    url = "{}?verification_code={}".format(reverse("social:complete", args=(backend.name,)), code.code)
    url = strategy.request.build_absolute_uri(url)
    send_mail(
        "Validate your account",
        f"Validate your account {url}",
        settings.EMAIL_FROM,
        [code.email],
        fail_silently=False,
    )
