import glob
import json
import math
import os

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.models import Q

from digest.models import Item


def check_exist_link(data, item):
    for info in data.get("links"):
        if info["link"] == item.link:
            return True
    else:
        return False


def save_dataset(data_items, name):
    if not data_items:
        return
    out_filepath = os.path.join(settings.DATASET_FOLDER, name)
    data = {"links": data_items}

    if not os.path.exists(os.path.dirname(out_filepath)):
        os.makedirs(os.path.dirname(out_filepath))

    with open(out_filepath, "w") as fio:
        json.dump(data, fio)


def save_queryset_dataset(queryset, name):
    if not queryset:
        return
    out_filepath = os.path.join(settings.DATASET_FOLDER, name)
    with open(out_filepath, "w") as fio:
        fio.write('{"links": [\n')
        items_cnt = queryset.count()
        for i, item in enumerate(queryset):
            fio.write(json.dumps(item.get_data4cls(status=True)))
            if i != items_cnt - 1:
                fio.write(",\n")
        fio.write("\n]}")


class Command(BaseCommand):
    help = "Create dataset"

    def add_arguments(self, parser):
        parser.add_argument("cnt_parts", type=int)  # сколько частей
        parser.add_argument("percent", type=int)  # сколько частей
        parser.add_argument("dataset_folder", type=str)  # ссылка на дополнительный датасет для объединения

    def handle(self, *args, **options):
        assert os.path.exists(options["dataset_folder"])
        additional_data = []
        for x in glob.glob("%s/*.json" % options["dataset_folder"]):
            with open(x) as fio:
                additional_data.extend(json.load(fio)["links"])
        # TODO additional_data is off

        query = Q()

        urls = [
            "allmychanges.com",
            "stackoverflow.com",
        ]
        for entry in urls:
            query = query | Q(link__contains=entry)

        active_news = Item.objects.filter(status="active").exclude(section=None).exclude(query)
        links = active_news.all().values_list("link", flat=True).distinct()
        non_active_news = Item.objects.exclude(link__in=links).exclude(query)

        items_ids = list(active_news.values_list("id", flat=True))
        items_ids.extend(non_active_news.values_list("id", flat=True))
        items_ids = list(set(items_ids))

        items = Item.objects.filter(id__in=items_ids).order_by("?")

        items_cnt = items.count()

        train_size = math.ceil(items_cnt * (options["percent"] / 100))
        test_size = items_cnt - train_size
        train_part_size = math.ceil(train_size / options["cnt_parts"])
        test_part_size = math.ceil(test_size / options["cnt_parts"])

        train_set = items[0:train_size]
        test_set = items[train_size + 1 :]
        save_function = save_queryset_dataset

        # items_data = [x.get_data4cls(status=True) for x in items]
        # items_data.extend(additional_data)
        # random.shuffle(items_data)
        #
        # train_set = items_data[:train_size]
        # test_set = items_data[train_size:]
        # save_function = save_dataset

        for part in range(options["cnt_parts"]):
            print("Create part {} (of {})".format(part, options["cnt_parts"]))
            train_name = f"train_{train_part_size}_{part}.json"
            test_name = f"test_{test_part_size}_{part}.json"

            save_function(
                train_set[part * train_part_size : (part + 1) * train_part_size],
                train_name,
            )

            save_function(
                test_set[part * test_part_size : (part + 1) * test_part_size],
                test_name,
            )
