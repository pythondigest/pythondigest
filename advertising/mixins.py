from django.views.generic.base import ContextMixin

from .models import get_ads


class AdsMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ads"] = get_ads()
        return context
