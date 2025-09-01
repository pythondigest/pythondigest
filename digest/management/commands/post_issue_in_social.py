"""

Example
python manage.py post_issue_in_social 467
"""

from urllib.parse import urljoin

from django.conf import settings
from django.core.management.base import BaseCommand

from digest.models import Issue
from digest.pub_digest import pub_to_all


def prepare_issue_news(issue: Issue):
    news = issue.item_set
    result = {}

    for x in news.filter(status="active").iterator():
        if x.section not in result:
            result[x.section] = []
        result[x.section].append(
            {
                "link": x.link,
                "title": x.title,
                "description": x.description,
                "tags": [],
            }
        )
    result = sorted(result.items(), key=lambda x: x[0].priority, reverse=True)
    result = [{"category": x.title, "news": y} for x, y in result]
    return result


class Command(BaseCommand):
    args = "no arguments!"
    help = "News import from external resources"

    def add_arguments(self, parser):
        parser.add_argument("issue", type=int)

    def handle(self, *args, **options):
        """
        Основной метод - точка входа
        """
        issue = Issue.objects.get(pk=options["issue"])
        site = settings.PROJECT_SITE

        issue_image_url = urljoin(site, "static/img/logo.png")
        if issue.image:
            issue_image_url = urljoin(site, issue.image.url)

        pub_to_all(
            issue.pk,
            issue.title,
            issue.announcement,
            urljoin(site, issue.link),
            issue_image_url,
            prepare_issue_news(issue),
        )
