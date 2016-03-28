# -*- encoding: utf-8 -*-
from django.conf import settings
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.utils import timezone

from digest.models import Issue, Item, Section


class IndexViewTest(TestCase):
    def test_context_var_items_if_has_related_not_active_items(self):
        date = timezone.now().date()
        issue = Issue.objects.create(title='Title 1', version=1,
                                     status='active',
                                     published_at=date)

        section = Section.objects.create(title='Section 1 title', priority=1)

        Item.objects.create(title='Item 1 title', link='pass@pass.com',
                            version=2,
                            section=section, issue=issue, status='pending')

        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['items']), [])

    def test_context_var_items_if_has_no_related_active_items(self):
        past = timezone.now().date() - timezone.timedelta(days=1)

        issue = Issue.objects.create(title='Title 1', version=1,
                                     status='active',
                                     published_at=past)
        Item.objects.create(title='Item 1 title', link='pass@pass.com',
                            version=2, issue=issue, status='active')

        Issue.objects.create(title='Title 2', version=1, status='active',
                             published_at=timezone.now().date())

        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['items']), [])

    def test_context_var_items_if_has_related_active_items(self):
        date = timezone.now().date()
        issue = Issue.objects.create(title='Title 1', version=1,
                                     status='active',
                                     published_at=date)

        section = Section.objects.create(title='Section 1 title', priority=1)

        item = Item.objects.create(title='Item 1 title', link='pass@pass.com',
                                   version=2,
                                   section=section, issue=issue,
                                   status='active')

        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['items']), [item])

    def test_context_var_items_ordering(self):
        date = timezone.now().date()
        issue = Issue.objects.create(title='Title 1', version=1,
                                     status='active',
                                     published_at=date)

        section1 = Section.objects.create(title='Section 1 title', priority=1)

        item1 = Item.objects.create(title='Item 1 title', link='pass@pass.com',
                                    version=2,
                                    section=section1, priority=2, issue=issue,
                                    status='active')

        item2 = Item.objects.create(title='Item 2 title', link='pass@pass.com',
                                    version=1,
                                    section=section1, priority=3, issue=issue,
                                    status='active')

        section2 = Section.objects.create(title='Section 2 title', priority=2)
        item3 = Item.objects.create(title='Item 3 title', link='pass@pass.com',
                                    version=1,
                                    section=section2, priority=1, issue=issue,
                                    status='active')

        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['items']), [item3, item2, item1])

    def test_context_var_issue_if_has_no_active_issues(self):
        Issue.objects.create(title='Title 1', version=1, status='draft')

        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['issue'], False)

    def test_context_var_issue_if_has_no_issues(self):
        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['issue'], False)

    # XXX bug - модель не требует поля image, а шаблон - да
    def test_context_var_issue_if_has_active_issues_without_published_at(self):
        issue = Issue.objects.create(title='Title 1', version=1,
                                     status='active')
        Issue.objects.create(title='Title 2', version=2, status='active')

        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['issue'], issue)

    # XXX bug - модель не требует поля image, а шаблон - да
    def test_context_var_issue_if_has_active_issues_with_filled_published_at_field(
            self):
        date = timezone.now().date()
        issue = Issue.objects.create(title='Title 1', version=1,
                                     status='active',
                                     published_at=date)

        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['issue'], issue)

    def test_context_var_active_menu_item(self):
        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['active_menu_item'], 'index')

    def test_template_used(self):
        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/index.html')

#
# class SitemapTest(TestCase):
#     def setUp(self):
#         self.url = reverse('frontend:sitemap')
#
#     def test_template_used(self):
#         response = self.client.get(self.url)
#
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'sitemap.html')
#
#     def test_content_type(self):
#         response = self.client.get(self.url)
#
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.content_type, 'text/xml')
#
#     def test_context_var_domain(self):
#         response = self.client.get(self.url)
#
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(
#             response.context['domain'],
#             'http://%s' %
#             settings.BASE_DOMAIN)
#
#     def test_context_var_record_if_no_active_issues_exists(self):
#         items = [
#             {
#                 'loc': '',
#                 'changefreq': 'weekly',
#             },
#             {
#                 'loc': reverse('digest:issues'),
#                 'changefreq': 'weekly',
#             },
#             {
#                 'loc': reverse('digest:feed'),
#                 'changefreq': 'daily',
#             },
#         ]
#
#         response = self.client.get(self.url)
#
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.context['records'], items)
#
#     def test_context_var_record_if_active_issues_exists(self):
#         items = [
#             {
#                 'loc': '',
#                 'changefreq': 'weekly',
#             },
#             {
#                 'loc': reverse('digest:issues'),
#                 'changefreq': 'weekly',
#             },
#             {
#                 'loc': reverse('digest:feed'),
#                 'changefreq': 'daily',
#             },
#         ]
#
#         response = self.client.get(self.url)
#
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.context['records'], items)
#

class IssuesListTest(TestCase):
    pass


class IssueViewTest(TestCase):
    pass


class NewsListTest(TestCase):
    pass


class AddNewsTest(TestCase):
    pass


class ViewEditorMaterialTest(TestCase):
    pass


class ItemViewTest(TestCase):
    pass
