from django.test import TestCase
from django.db.utils import IntegrityError
from django.contrib.auth import get_user_model
from django.utils import timezone
User = get_user_model()

from frontend.models import EditorMaterial, Tip


class EditorMaterialTest(TestCase):

    @classmethod
    def setUpTestData(cls):

        cls.user = User.objects.create_user(username='haxor', password='1337')

        cls.em1 = EditorMaterial.objects.create(title='Заголовок 1',
            slug='slug1', section='news', status='draft', announce='Анонс 1',
            contents='Текст 1', user=cls.user
        )

        cls.em2 = EditorMaterial.objects.create(title='Заголовок 2',
            slug='slug2', section='news', status='draft', announce='Анонс 2',
            contents='Текст 2', user=cls.user
        )

        cls.em3 = EditorMaterial.objects.create(title='Заголовок 3',
            slug='slug3', section='landing', status='draft', announce='Анонс 3',
            contents='Текст 3', user=cls.user
        )

    def test_str(self):

        self.assertEqual(str(self.em1), 'Заголовок 1')

    def test_slug_and_section_is_unique_together(self):

        self.em2.slug = 'slug1'
        self.em2.section = 'news'

        with self.assertRaises(IntegrityError):
            self.em2.save()

    def test_created_at_field_is_auto_now_add(self):
        past = timezone.now()
        em = EditorMaterial.objects.create(title='Заголовок',
            slug='slug', section='landing', status='draft', announce='Анонс',
            contents='Текст', user=self.user
        )

        self.assertGreater(em.created_at, past)


class TipTest(TestCase):

    @classmethod
    def setUpTestData(cls):

        cls.tip1 = Tip.objects.create(text='advice 1')
        cls.tip2 = Tip.objects.create(text='advice 2', active=False)

    def test_str(self):

        self.assertEqual(str(self.tip1), 'advice 1')
