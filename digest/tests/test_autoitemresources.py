# -*- encoding: utf-8 -*-

from django.test import TestCase

from digest.models import AutoImportResource, Resource


def create_resource(**kwargs):
    kwargs['title'] = kwargs.get('title', 'Test')
    kwargs['link'] = kwargs.get('link', 'http://pythondigest.ru')

    return AutoImportResource.objects.create(**kwargs)


class AutoImportResourceTest(TestCase):
    def test_filter(self):
        create_resource()
        create_resource(title='test2', type_res='rss', link='https://python3.ru')
        create_resource(title='test3', in_edit=True, link='https://python7.ru')
        create_resource(title='test4', type_res='rss', in_edit=True, link='https://python4.ru')
        self.assertEqual(AutoImportResource.objects.count(), 4)
        self.assertEqual(AutoImportResource.objects.filter(type_res='twitter').count(), 2)
        self.assertEqual(AutoImportResource.objects.filter(type_res='twitter', in_edit=False).count(), 1)
        self.assertEqual(AutoImportResource.objects.filter(type_res='rss').count(), 2)
        self.assertEqual(AutoImportResource.objects.filter(type_res='rss', in_edit=False).count(), 1)

    def test_resource_creation(self):
        resource = create_resource()
        self.assertTrue(isinstance(resource, AutoImportResource))
        self.assertEqual(resource.__str__(), resource.title)
        self.assertEqual(resource.type_res, 'twitter')
        self.assertEqual(resource.language, 'en')

    def test_resource_language(self):
        resource = create_resource(language='ru')
        self.assertEqual(resource.language, 'ru')

    def test_resource_type_res(self):
        resource = create_resource()
        self.assertEqual(resource.type_res, 'twitter')

        resource.type_res = 'rss'
        self.assertEqual(resource.type_res, 'rss')

        resource = create_resource(title='Test2', type_res='rss', link='https://python.ru2')
        self.assertEqual(resource.type_res, 'rss')

    def test_with_resource(self):
        res = Resource.objects.create(title='Test', link='https://python.ru')
        resource = create_resource(resource=res)
        self.assertEqual(resource.resource, res)
