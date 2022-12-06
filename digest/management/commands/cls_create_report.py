import csv
import json
import os

import requests
from django.conf import settings
from django.core.management.base import BaseCommand

from digest.management.commands.cls_split_dataset import load_data_from_folder


class Command(BaseCommand):
    help = "Create dataset"

    def add_arguments(self, parser):
        parser.add_argument("dataset_test_folder", type=str)
        parser.add_argument("out_path", type=str)

    def handle(self, *args, **options):
        """
        Основной метод - точка входа
        """
        items = load_data_from_folder(options["dataset_test_folder"])

        part_size = 100
        cur_part = 0
        url = "{}/{}".format(settings.CLS_URL_BASE, "api/v1.0/classify/")

        cnt = len(items)
        print(cnt)
        cls_data = []
        while part_size * cur_part < cnt:
            print(cur_part)

            links_items = items[part_size * cur_part : part_size * (cur_part + 1)]
            data = {"links": links_items}

            try:
                resp = requests.post(url, data=json.dumps(data))
                resp_data = {}
                for x in resp.json()["links"]:
                    for key, value in x.items():
                        resp_data[key] = value
            except (
                requests.exceptions.RequestException,
                requests.exceptions.Timeout,
                requests.exceptions.TooManyRedirects,
            ) as e:
                resp_data = None

            for x in links_items:
                if resp_data is None:
                    status = False
                else:
                    status = resp_data.get(x.get("link"), False)

                cls_data.append(
                    {
                        "link": x.get("link"),
                        "moderator": x["data"].get("label"),
                        "classificator": status,
                    }
                )
            cur_part += 1

        out_path = os.path.abspath(os.path.normpath(options["out_path"]))
        if not os.path.isdir(os.path.dirname(out_path)):
            os.makedirs(os.path.dirname(out_path))

        with open(out_path, "w") as fio:
            fieldnames = cls_data[0].keys()
            writer = csv.DictWriter(fio, fieldnames=fieldnames)
            headers = {n: n for n in fieldnames}
            writer.writerow(headers)
            for i in cls_data:
                writer.writerow(i)
