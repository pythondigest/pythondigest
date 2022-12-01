from django.core.management.base import BaseCommand

from digest.models import ItemClsCheck


class Command(BaseCommand):
    help = "lala"

    def handle(self, *args, **options):
        for x in ItemClsCheck.objects.all():
            x.check_cls(force=True)
