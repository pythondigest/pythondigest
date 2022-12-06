import glob
import json
import math
import os
import random

from django.core.management.base import BaseCommand

from digest.management.commands.cls_create_dataset import save_dataset


def load_data_from_folder(folder):
    assert os.path.exists(folder)
    result = []
    for x in glob.glob("%s/*.json" % folder):
        with open(x) as fio:
            result.extend(json.load(fio)["links"])
    return result


class Command(BaseCommand):
    help = "Create dataset"

    def add_arguments(self, parser):
        parser.add_argument("cnt_parts", type=int)  # сколько частей
        parser.add_argument("percent", type=int)  # сколько частей
        parser.add_argument("items_folder", type=str)
        parser.add_argument("add_folder", type=str)

    def handle(self, *args, **options):
        """
        Основной метод - точка входа
        """

        items_data = []
        items_data.extend(load_data_from_folder(options["add_folder"]))
        items_data.extend(load_data_from_folder(options["items_folder"]))

        random.shuffle(items_data)
        items_cnt = len(items_data)

        train_size = math.ceil(items_cnt * (options["percent"] / 100))
        test_size = items_cnt - train_size
        train_part_size = math.ceil(train_size / options["cnt_parts"])
        test_part_size = math.ceil(test_size / options["cnt_parts"])

        train_set = items_data[:train_size]
        test_set = items_data[train_size:]

        for part in range(options["cnt_parts"]):
            train_name = f"train_{train_part_size}_{part}.json"
            test_name = f"test_{test_part_size}_{part}.json"
            save_dataset(
                train_set[part * train_part_size : (part + 1) * train_part_size],
                train_name,
            )
            save_dataset(
                test_set[part * test_part_size : (part + 1) * test_part_size],
                test_name,
            )
