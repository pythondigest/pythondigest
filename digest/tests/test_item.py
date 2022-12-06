from django.test import TestCase

from digest.models import Item, Section


class ItemModelTest(TestCase):
    def test_type(self):
        section = Section(title="Статьи")

        object = Item(title="Title1", link="https://pythondigest.ru", section=section)
