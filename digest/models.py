# -*- coding: utf-8 -*-
import datetime
import json
# import the logging library
import logging
import os

import requests
import requests.exceptions
from django_remdow.templatetags.remdow import (
    remdow_img_center,
    remdow_img_local,
    remdow_img_responsive,
    remdow_lazy_img,
)
from readability.readability import Document, Unparseable
from taggit.models import GenericTaggedItemBase, TagBase
from taggit_autosuggest.managers import TaggableManager

from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import QueryDict
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from frontend.models import Tip

# Get an instance of a logger
logger = logging.getLogger(__name__)
ISSUE_STATUS_CHOICES = (('active', _('Active')), ('draft', _('Draft')),)
ISSUE_STATUS_DEFAULT = 'draft'
ITEM_STATUS_DEFAULT = 'pending'

ITEM_STATUS_CHOICES = (
    ('pending', _('Pending')),
    ('active', _('Active')),
    ('draft', _('Draft')),
    ('moderated', _('Moderated')),
    ('autoimport', _('Imported')),
    ('queue', _('In queue')),
)

SECTION_STATUS_CHOICES = (('pending', _('Pending')),
                          ('active', _('Active')),)
SECTION_STATUS_DEFAULT = 'active'

ITEM_LANGUAGE_CHOICES = (('ru', _('Russian')), ('en', _('English')),)
ITEM_LANGUAGE_DEFAULT = 'en'
LIBRARY_SECTIONS = None
TYPE_RESOURCE_DEFAULT = 'twitter'
TYPE_RESOURCE = (('twitter', _('Twitter feed')),
                 ('rss', _('RSS feed')),)


def build_url(*args, **kwargs):
    params = kwargs.pop('params', {})
    url = reverse(*args, **kwargs)
    if not params:
        return url

    query_dict = QueryDict('', mutable=True)
    for k, v in params.items():
        if type(v) is list:
            query_dict.setlist(k, v)
        else:
            query_dict[k] = v

    return url + '?' + query_dict.urlencode()


def load_library_sections():
    global LIBRARY_SECTIONS
    titles = [
        'Интересные проекты, инструменты, библиотеки',
        'Релизы'
    ]
    try:
        LIBRARY_SECTIONS = [Section.objects.get(title=title) for title in
                            titles]
    except (ObjectDoesNotExist, Section.DoesNotExist):
        LIBRARY_SECTIONS = []


def get_start_end_of_week(dt):
    start = dt - datetime.timedelta(days=dt.weekday())
    end = start + datetime.timedelta(days=6)
    return start, end


class Keyword(TagBase):
    """
    Keyword is a word for SEO optimization
    """

    class Meta:
        verbose_name = _('Keyword')
        verbose_name_plural = _('Keywords')


class KeywordGFK(GenericTaggedItemBase):
    tag = models.ForeignKey(Keyword,
                            related_name='%(app_label)s_%(class)s_items',
                            on_delete=models.CASCADE)


class Issue(models.Model):
    """
    The issue of the digest.
    It is collection of `Items`
    """
    title = models.CharField(
        verbose_name=_('Title'), max_length=255)
    description = models.TextField(verbose_name=_('Description'), blank=True)
    announcement = models.TextField(verbose_name=_('Announcement'), blank=True)
    image = models.ImageField(
        verbose_name=_('Image'), upload_to='issues', blank=True)
    date_from = models.DateField(
        verbose_name=_('Start date'), null=True, blank=True)
    date_to = models.DateField(
        verbose_name=_('End date'), null=True, blank=True)
    published_at = models.DateField(
        verbose_name=_('Publication date'), null=True, blank=True)
    status = models.CharField(
        verbose_name=_('Status'),
        max_length=10,
        choices=ISSUE_STATUS_CHOICES,
        default=ISSUE_STATUS_DEFAULT)
    trend = models.CharField(
        verbose_name=_('Trend'), blank=True, max_length=255)
    last_item = models.IntegerField(
        verbose_name=_('Latest moderated Item'), blank=True, null=True)

    def __str__(self):
        return self.title

    @property
    def link(self):
        return reverse('digest:issue_view', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-pk']
        verbose_name = _('Issue of digest')
        verbose_name_plural = _('Issues of digest')


class Section(models.Model):
    """
    Section is a category of news-item
    """
    title = models.CharField(
        verbose_name=_('Title'), max_length=255)
    priority = models.PositiveIntegerField(
        verbose_name=_('Priority'), default=0)
    status = models.CharField(
        verbose_name=_('Status'), max_length=10,
        choices=SECTION_STATUS_CHOICES, default=SECTION_STATUS_DEFAULT)
    icon = models.CharField(
        verbose_name=_('Icon'), max_length=255, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-pk']
        verbose_name = _('Section')
        verbose_name_plural = _('Sections')


class Resource(models.Model):
    """
    A script extracts news from `Resource`
    """
    title = models.CharField(
        verbose_name=_('Title'), max_length=255)
    description = models.TextField(
        verbose_name=_('Description'), blank=True)
    link = models.URLField(
        verbose_name=_('URL'), max_length=255)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Resource')
        verbose_name_plural = _('Resources')


class Item(models.Model):
    """
    Item is a content, is a link
    """
    section = models.ForeignKey(
        Section,
        verbose_name=_('Section'), null=True, blank=True,
        on_delete=models.CASCADE)
    title = models.CharField(
        verbose_name=_('Title'), max_length=255)
    is_editors_choice = models.BooleanField(
        verbose_name=_('Is editors choice'), default=True)
    description = models.TextField(
        verbose_name=_('Description'), blank=True)
    issue = models.ForeignKey(
        Issue,
        on_delete=models.CASCADE,
        verbose_name=_('Issue of digest'), null=True, blank=True)
    resource = models.ForeignKey(
        Resource,
        on_delete=models.CASCADE,
        verbose_name=_('Resource'), null=True, blank=True)
    link = models.URLField(
        verbose_name=_('URL'), max_length=255)
    additionally = models.CharField(
        verbose_name=_('Additional info'),
        max_length=255, blank=True, null=True)
    related_to_date = models.DateField(
        verbose_name=_('Date'),
        help_text=_('For example, publication date of the news on the source'),
        default=datetime.datetime.today)
    status = models.CharField(
        verbose_name=_('Status'), max_length=10,
        choices=ITEM_STATUS_CHOICES, default=ITEM_STATUS_DEFAULT)
    language = models.CharField(
        verbose_name='Язык новости', max_length=2,
        choices=ITEM_LANGUAGE_CHOICES, default=ITEM_LANGUAGE_DEFAULT)
    created_at = models.DateField(
        verbose_name=_('Created date'), auto_now_add=True)
    modified_at = models.DateTimeField(
        verbose_name=_('modified date'), null=True, blank=True)
    activated_at = models.DateTimeField(
        verbose_name=_('Activated date'), default=datetime.datetime.now)
    priority = models.PositiveIntegerField(
        verbose_name=_('Priority'), default=0)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('Who added item'), editable=False,
        null=True, blank=True)
    article_path = models.FilePathField(
        verbose_name=_('Article path'),
        blank=True,
        path=settings.DATASET_ROOT,
    )
    tags = TaggableManager(blank=True)
    keywords = TaggableManager(
        verbose_name=_('Keywords'), through=KeywordGFK, blank=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._disable_signals = False

    def save(self, *args, **kwargs):
        try:
            if self.issue is None and self.created_at is not None:
                date_from, date_to = get_start_end_of_week(self.created_at)
                issue = Issue.objects.filter(date_from=date_from,
                                             date_to=date_to)
                if issue.count() == 0:
                    # если нет выпуска, то создадим
                    old_issue = Issue.objects.latest('date_to')
                    cnt_issue = int(old_issue.title.replace('Выпуск ', '')) + 1
                    new_issue = Issue(title='Выпуск %s' % cnt_issue,
                                      date_from=date_from,
                                      date_to=date_to, )
                    new_issue.save()
                    self.issue = new_issue
                elif issue.count() == 1:
                    self.issue = issue[0]
                else:
                    raise Exception('Many issues are on one week')

        except Exception as e:
            logger.error('Many issues are on one week: {0}'.format(e))
        super(Item, self).save(*args, **kwargs)

    def save_without_signals(self):
        """
        This allows for updating the model from code running inside post_save()
        signals without going into an infinite loop:
        """
        self._disable_signals = True
        self.save()
        self._disable_signals = False

    @property
    def cls_check(self):
        try:
            item = ItemClsCheck.objects.get(item=self)
            item.check_cls()
        except (ObjectDoesNotExist, ItemClsCheck.DoesNotExist):
            item = ItemClsCheck(item=self)
            item.save()
            item.check_cls(force=True)
        return item.score

    @property
    def link_type(self):
        global LIBRARY_SECTIONS
        if LIBRARY_SECTIONS is None:
            load_library_sections()
        if any((x == self.section_id for x in LIBRARY_SECTIONS)):
            return 'library'
        else:
            return 'article'

    @property
    def text(self):
        nonempty_path = self.article_path is not None and self.article_path
        if nonempty_path and os.path.exists(
            self.article_path):
            with open(self.article_path, 'r') as fio:
                result = fio.read()
        else:
            try:
                resp = requests.get(self.link)
                text = resp.text
                try:
                    result = Document(text,
                                      min_text_length=50,
                                      positive_keywords=','.join(
                                          settings.DATASET_POSITIVE_KEYWORDS),
                                      negative_keywords=','.join(
                                          settings.DATASET_NEGATIVE_KEYWORDS)
                                      ).summary()
                except Unparseable:
                    result = text
            except (KeyError,
                    requests.exceptions.RequestException,
                    requests.exceptions.Timeout,
                    requests.exceptions.TooManyRedirects) as e:
                result = ''
            self.article_path = os.path.join(settings.DATASET_ROOT,
                                             '{0}.html'.format(self.id))
            with open(self.article_path, 'w') as fio:
                fio.write(result)
            self.save()
        return result

    def get_data4cls(self, status=False):
        result = {
            'link': self.link,
            'data': {
                'language': self.language,
                'title': self.title,
                'description': self.description,
                'article': self.text,
                'type': self.link_type,
            }
        }
        if status:
            result['data']['label'] = self.status == 'active'
        return result

    data4cls = property(get_data4cls)

    @property
    def internal_link(self):
        return reverse('digest:item', kwargs={'pk': self.pk})

    @property
    def tags_as_links(self):
        return [(x.name, build_url('digest:feed', params={'tag': x.name}))
                for x in self.tags.all()]

    @property
    def tags_as_str(self):
        if self.tags and self.tags.all():
            result = ','.join([x.name for x in self.tags.all()])
        else:
            result = 'Without tag'
        return result

    @property
    def keywords_as_str(self):
        return ', '.join(list({x.name for x in self.keywords.all()})[:13])

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('News')
        verbose_name_plural = _('News')


class ItemClsCheck(models.Model):
    item = models.OneToOneField(Item, on_delete=models.CASCADE, verbose_name=_('News'))
    last_check = models.DateTimeField(
        verbose_name=_('Last check time'), auto_now=True)
    score = models.BooleanField(verbose_name=_('Score'), default=False)

    def check_cls(self, force=False):
        # print('Run check: {}'.format(self.pk))
        prev_data = datetime.datetime.now() - datetime.timedelta(days=10)
        if force or self.last_check <= prev_data:

            try:
                url = '{0}/{1}'.format(settings.CLS_URL_BASE,
                                       'api/v1.0/classify/')
                resp = requests.post(url,
                                     data=json.dumps({'links': [
                                         self.item.data4cls
                                     ]}))
                self.score = resp.json()['links'][0].get(self.item.link, False)
            except (requests.exceptions.RequestException,
                    requests.exceptions.Timeout,
                    requests.exceptions.TooManyRedirects) as e:
                self.score = False
            # print('Real run check: {}'.format(self.pk))
            self.save()

    def __str__(self):
        return '{0} - {1} ({2})'.format(
            str(self.item), self.score, self.last_check)

    class Meta:
        verbose_name = _('Classifier analysis')
        verbose_name_plural = _('Classifier analysis')


class AutoImportResource(models.Model):
    """

    """
    title = models.CharField(
        verbose_name=_('Title'), max_length=255)
    link = models.URLField(
        verbose_name=_('URL'), max_length=255, unique=True)
    type_res = models.CharField(
        verbose_name=_('Type'), max_length=255,
        choices=TYPE_RESOURCE, default=TYPE_RESOURCE_DEFAULT)
    resource = models.ForeignKey(
        Resource,
        on_delete=models.CASCADE,
        verbose_name=_('Source'), null=True, blank=True)
    incl = models.CharField(
        verbose_name=_('Required content'),
        max_length=255, help_text='Условие отбора новостей <br /> \
                   Включение вида [text] <br /> \
                   Включение при выводе будет удалено',
        blank=True)
    excl = models.TextField(
        verbose_name='Exceptions',
        help_text='List of exceptions, indicate by ", "',
        blank=True)
    in_edit = models.BooleanField(
        verbose_name=_('On testing'), default=False)
    language = models.CharField(
        verbose_name=_('Language of content'), max_length=2,
        choices=ITEM_LANGUAGE_CHOICES, default=ITEM_LANGUAGE_DEFAULT)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('News source')
        verbose_name_plural = _('News sources')


class Package(models.Model):
    name = models.CharField(verbose_name=_('Name'), max_length=255)
    description = models.TextField(
        verbose_name=_('Description'), blank=True)
    link = models.URLField(
        verbose_name=_('URL'), max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Package')
        verbose_name_plural = _('Packages')


class ParsingRules(models.Model):
    IF_ELEMENTS = (('title', 'Заголовок новости'), ('link', 'Url новости'),
                   ('content', 'Текст новости'),
                   ('description', 'Описание новости'),
                   ('http_code', 'HTTP Code'),)

    IF_ACTIONS = (('equal', 'Равен'), ('contains', 'Содержит'),
                  ('not_equal', 'Не равен'), ('regex', 'Regex match'),)

    THEN_ELEMENT = (('title', 'Заголовок новости'),
                    ('description', 'Описание новости'),
                    ('section', 'Раздел'), ('status', 'Статус'),
                    ('tags', 'Тэг новости'),)

    THEN_ACTION = (('set', 'Установить'), ('add', 'Добавить'),
                   ('remove', 'Удалить часть строки'),)

    title = models.CharField(
        verbose_name=_('Title'), max_length=255)
    is_activated = models.BooleanField(
        verbose_name=_('Is active'), default=True)
    if_element = models.CharField(
        verbose_name=_('IF element'), max_length=255,
        choices=IF_ELEMENTS, default='item_title')
    if_action = models.CharField(
        verbose_name=_('IF condition'), max_length=255,
        choices=IF_ACTIONS, default='consist')
    if_value = models.CharField(verbose_name=_('IF value'), max_length=255)
    then_element = models.CharField(
        verbose_name=_('THEN element'), max_length=255,
        choices=THEN_ELEMENT, default='item_title')
    then_action = models.CharField(
        verbose_name=_('THEN action'), max_length=255,
        choices=THEN_ACTION, default='item_title')
    then_value = models.CharField(
        verbose_name=_('THEN value'), max_length=255)
    weight = models.PositiveIntegerField(
        verbose_name=_('Weight'), default=100)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Processing rule')
        verbose_name_plural = _('Processing rules')
        ordering = ['-weight']


@receiver(post_save, sender=Item)
def update_cls_score(instance, **kwargs):
    if not settings.CLS_ENABLED:
        return

    if instance._disable_signals:
        return

    try:
        item = ItemClsCheck.objects.get(item=instance)
        item.check_cls(False)
    except (ObjectDoesNotExist, ItemClsCheck.DoesNotExist):
        item = ItemClsCheck(item=instance)
        item.save()
        item.check_cls(True)


@receiver(post_save, sender=Item)
def run_remdow(instance, **kwargs):
    if instance._disable_signals:
        return

    description = instance.description
    if description is None:
        description = ''

    if "img" not in description:
        return

    instance.description = \
        remdow_lazy_img(
            remdow_img_responsive(
                remdow_img_center(
                    remdow_img_local(description))))
    instance.save_without_signals()
