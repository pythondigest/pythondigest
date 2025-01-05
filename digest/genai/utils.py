from django.conf import settings

from .chad import Chad


def get_llm():
    return Chad(
        temperature=0,
        chad_api_key=settings.CHAD_API_KEY,
        model=settings.CHAD_API_MODEL,
    )
