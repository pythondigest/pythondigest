"""
Собираем датасет для обучения и тестирования классификатора

python manage.py create_dataset 30 80
"""

import datetime
import json
import math
import os

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.models import Q
from django.db.models.manager import BaseManager
from tqdm import tqdm

from digest.models import Item


def get_queryset_for_dataset():
    query = Q()
    urls = [
        "allmychanges.com",
        "stackoverflow.com",
    ]
    for entry in urls:
        query = query | Q(link__contains=entry)
    N_YEARS = 5
    check_period = datetime.datetime.now() - datetime.timedelta(days=365 * N_YEARS)
    return Item.objects.filter(created_at__gte=check_period).exclude(query).order_by("-pk")


def create_dataset(queryset_items: BaseManager[Item], file_path: str):
    if not queryset_items:
        return

    result = []

    with tqdm(total=queryset_items.count()) as t:
        for item in queryset_items.iterator():
            t.update(1)

            if settings.DATASET_IGNORE_EMPTY_PAGES and not item.is_exists_text:
                continue

            item_data = item.get_data4cls(status=True)
            if not item_data or not item_data.get("data").get("article"):
                continue

            result.append(item_data)

    if result:
        with open(file_path, "w") as fio:
            json.dump({"links": result}, fio)


class Command(BaseCommand):
    help = "Create dataset"

    def add_arguments(self, parser):
        # на сколько частей разбить обучение
        parser.add_argument("train_parts", type=int)
        # какого размера обучающая выборка
        parser.add_argument("train_percent", type=int)

    def handle(self, *args, **options):
        """
        Основной метод - точка входа
        """

        dataset_queryset = get_queryset_for_dataset()

        items_cnt = dataset_queryset.count()
        train_size = math.ceil(items_cnt * (options["train_percent"] / 100))
        # test_size = items_cnt - train_size

        train_part_size = math.ceil(train_size / options["train_parts"])

        train_set = dataset_queryset[:train_size]
        test_set = dataset_queryset[train_size:]

        for part in range(options["train_parts"]):
            print(f"Work with {part} part....")
            name = f"data_{train_part_size}_{part}.json"

            file_path = os.path.join(settings.DATASET_ROOT, name)

            queryset: BaseManager[Item] = train_set[part * train_part_size : (part + 1) * train_part_size]
            create_dataset(queryset, file_path)

        with open(os.path.join(settings.DATASET_ROOT, "test_set_ids.txt"), "w") as fio:
            fio.writelines(["%s\n" % x for x in test_set.values_list("id", flat=True)])
