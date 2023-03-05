import csv
import os

from django.core.management.base import BaseCommand

from digest.models import ItemClsCheck


class Command(BaseCommand):
    help = "Create dataset"

    def add_arguments(self, parser):
        parser.add_argument("out_path", type=str)
        parser.add_argument("input_path", type=str)

    def handle(self, *args, **options):
        """
        Основной метод - точка входа
        """
        data = []
        ids = []

        if os.path.isfile(options["input_path"]):
            with open(options["input_path"]) as fio:
                ids = [int(x.strip()) for x in fio.readlines()]

        for x in ItemClsCheck.objects.filter(item__id__in=ids):
            data.append(
                {
                    "link": x.item.link,
                    "moderator": x.item.status == "active",
                    "classificator": x.status,
                }
            )
        out_path = os.path.abspath(os.path.normpath(options["out_path"]))
        if not os.path.isdir(os.path.dirname(out_path)):
            os.makedirs(os.path.dirname(out_path))

        with open(out_path, "w") as fio:
            fieldnames = data[0].keys()
            writer = csv.DictWriter(fio, fieldnames=fieldnames)
            headers = {n: n for n in fieldnames}
            writer.writerow(headers)
            for i in data:
                writer.writerow(i)
