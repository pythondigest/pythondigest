import os

from django.conf import settings
from django.core.management.base import BaseCommand

from digest.models import Item


def get_article(item):
    path: str = os.path.join(settings.PAGES_ROOT, f"{item.id}.html")
    with open(path, "w") as fio:
        try:
            text = item.text
        except Exception:
            text = ""

        fio.write(text)
        item.article_path = path
        item.save()
    return item.link


class Command(BaseCommand):
    help = "Create dataset"

    def handle(self, *args, **options):
        """
        Основной метод - точка входа
        """
        if not os.path.isdir(settings.DATASET_ROOT):
            os.makedirs(settings.DATASET_ROOT)

        for item in Item.objects.all():
            path_incorrect = item.article_path is None or not item.article_path
            path_exists = os.path.exists(item.article_path)
            if path_incorrect or not path_exists:
                get_article(item)
