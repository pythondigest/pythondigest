import json
import math
import os

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.models import Q
from django.db.models.manager import BaseManager

from digest.models import Item


def check_exist_link(data: dict, item: Item):
    for info in data.get("links"):
        if info["link"] == item.link:
            return True
    else:
        return False


def create_dataset(queryset_items: BaseManager[Item], name: str):
    if not queryset_items:
        return
    out_filepath = os.path.join(settings.DATASET_FOLDER, name)
    data = {"links": [x.get_data4cls(status=True) for x in queryset_items]}

    if not os.path.exists(os.path.dirname(out_filepath)):
        os.makedirs(os.path.dirname(out_filepath))

    with open(out_filepath, "w") as fio:
        json.dump(data, fio)


class Command(BaseCommand):
    help = "Create dataset"

    def add_arguments(self, parser):
        parser.add_argument("train_parts", type=int)  # на сколько частей разбить обучение
        parser.add_argument("train_percent", type=int)  # какого размера обучающая выборка

    def handle(self, *args, **options):
        """
        Основной метод - точка входа
        """

        query = Q()

        urls = [
            "allmychanges.com",
            "stackoverflow.com",
        ]
        for entry in urls:
            query = query | Q(link__contains=entry)

        items = Item.objects.exclude(query).order_by("?")

        items_cnt = items.count()
        train_size = math.ceil(items_cnt * (options["train_percent"] / 100))
        # test_size = items_cnt - train_size

        train_part_size = math.ceil(train_size / options["train_parts"])

        train_set = items[:train_size]
        test_set = items[train_size:]

        for part in range(options["train_parts"]):
            name = f"data_{train_part_size}_{part}.json"
            queryset: BaseManager[Item] = train_set[part * train_part_size : (part + 1) * train_part_size]
            create_dataset(queryset, name)

        with open(os.path.join(settings.DATASET_FOLDER, "test_set_ids.txt"), "w") as fio:
            fio.writelines(["%s\n" % x for x in test_set.values_list("id", flat=True)])
