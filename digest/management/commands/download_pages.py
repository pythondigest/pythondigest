"""
Скачиваем html копии страниц новостей

python manage.py download_pages
"""

import os

from django.conf import settings
from django.core.management.base import BaseCommand
from tqdm import tqdm

from digest.models import Item

from .create_dataset import get_queryset_for_dataset


def download_item(item: Item) -> str:
    path: str = os.path.join(settings.PAGES_ROOT, f"{item.id}.html")
    with open(path, "w") as fio:
        try:
            # in this property i download files
            text = item.text
        except Exception:
            text = ""
            return

        fio.write(text)
        item.article_path = path
        item.save()
    return item.link


class Command(BaseCommand):
    help = "Download html pages of items"

    def handle(self, *args, **options):
        dataset_queryset = get_queryset_for_dataset()

        with tqdm(total=dataset_queryset.count()) as t:
            for item in dataset_queryset.iterator():
                if not item.is_exists_text:
                    download_item(item)

                t.update(1)
