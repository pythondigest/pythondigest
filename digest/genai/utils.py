from django.conf import settings
from langchain_openai import ChatOpenAI

from .chad import Chad


def get_llm(temperature: float = 0):
    if settings.LLM_PROVIDER == "openai":
        return ChatOpenAI(
            model=settings.OPENAI_API_MODEL,
            base_url=settings.OPENAI_BASE_URL,
            api_key=settings.OPENAI_API_KEY,
            temperature=temperature,
        )
    elif settings.LLM_PROVIDER == "chad":
        return Chad(
            temperature=temperature,
            chad_api_key=settings.CHAD_API_KEY,
            model=settings.CHAD_API_MODEL,
        )
    else:
        raise ValueError(f"Invalid LLM provider: {settings.LLM_PROVIDER}")
