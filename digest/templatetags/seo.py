from django import template
from django.db.models import Model

from conf.meta import BaseModelMeta as ModelMeta

register = template.Library()


@register.simple_tag(takes_context=True)
def default_meta(context):
    """
    Готовим метаданные для страницы

    Если есть объект в контексте, то используем его метаданные
    Иначе используем метаданные по умолчанию
    """

    request = context.get("request")

    object: Model | None = context.get("object")

    if object and hasattr(object, "get_meta"):
        return object.as_meta(request)

    return ModelMeta().as_meta(request)
