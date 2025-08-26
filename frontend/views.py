# import the logging library
import datetime
import logging

from django.conf import settings
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import TemplateView

from advertising.mixins import AdsMixin
from digest.mixins import CacheMixin, FavoriteItemsMixin, FeedItemsMixin
from digest.models import Issue, Item
from frontend.models import EditorMaterial

# Get an instance of a logger
logger = logging.getLogger(__name__)


class Sitemap(TemplateView):
    content_type = "text/xml"
    template_name = "sitemap.html"
    protocol = "https"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        items = [
            {"loc": "", "changefreq": "weekly"},
            {"loc": reverse("digest:issues"), "changefreq": "weekly"},
            {"loc": reverse("digest:feed"), "changefreq": "daily"},
        ]

        for issue in Issue.objects.filter(status="active"):
            items.append({"loc": issue.get_absolute_url(), "changefreq": "weekly"})

        for item in Item.objects.filter(status="active", activated_at__lte=datetime.datetime.now())[:20000]:
            items.append({"loc": item.get_absolute_url(), "changefreq": "weekly"})

        ctx.update({"records": items, "domain": f"https://{settings.BASE_DOMAIN}"})

        return ctx


class IndexView(CacheMixin, FavoriteItemsMixin, FeedItemsMixin, AdsMixin, TemplateView):
    """Главная страница."""

    template_name = "pages/index.html"
    model = Issue
    context_object_name = "index"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        issue = False
        try:
            issue = self.model.objects.filter(status="active").latest("published_at")
        except Issue.DoesNotExist as e:
            logger.warning(f"Not found active Issue for index page: {str(e)}")

        items = []
        if issue:
            items = (
                issue.item_set.filter(status="active")
                .exclude(section=None)
                .only(
                    "title",
                    "description",
                    "tags",
                    "section",
                    "link",
                    "language",
                    "priority",
                    "issue",
                    "additionally",
                )
                .select_related("section")
                .prefetch_related("tags")
                .order_by("-section__priority", "-priority")
            )

        context.update(
            {
                "object": issue,
                "issue": issue,
                "items": items,
                "active_menu_item": "index",
            }
        )
        return context


class FriendsView(TemplateView):
    template_name = "pages/friends.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_menu_item"] = "friends"
        return context


class ViewEditorMaterial(TemplateView):
    template_name = "old/editor_material_view.html"

    def get_context_data(self, **kwargs):
        section = kwargs.get("section", "landing")
        slug = kwargs.get("slug")

        material = get_object_or_404(EditorMaterial, slug=slug, section=section, status="active")

        return {"material": material}
