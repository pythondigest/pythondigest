# -*- coding: utf-8 -*-
import datetime

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from concurrency.fields import IntegerVersionField
from django.db import models

ISSUE_STATUS_CHOICES = (
    ('active', u'Активный'),
    ('draft', u'Черновик'),
)


def get_start_end_of_week(dt):
    start = dt - datetime.timedelta(days=dt.weekday())
    end = start + datetime.timedelta(days=6)
    return start, end


class Issue(models.Model):
    '''
    Выпуск дайджеста
    '''
    title = models.CharField(
        max_length=255,
        verbose_name=u'Заголовок',
    )
    description = models.TextField(
        verbose_name=u'Описание',
        null=True, blank=True,
    )
    image = models.ImageField(
        verbose_name=u'Постер',
        upload_to='issues',
        null=True, blank=True,
    )
    date_from = models.DateField(
        verbose_name=u'Начало освещаемого периода',
        null=True, blank=True,
    )
    date_to = models.DateField(
        verbose_name=u'Завершение освещаемого периода',
        null=True, blank=True,
    )
    published_at = models.DateField(
        verbose_name=u'Дата публикации',
        null=True, blank=True,
    )
    status = models.CharField(
        verbose_name=u'Статус',
        max_length=10,
        choices=ISSUE_STATUS_CHOICES,
        default='draft',
    )
    version = IntegerVersionField(
        verbose_name=u'Версия'
    )

    def __unicode__(self):
        return self.title

    @property
    def link(self):
        return reverse('frontend:issue_view', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-pk']
        verbose_name = u'Выпуск дайджеста'
        verbose_name_plural = u'Выпуски дайджеста'


SECTION_STATUS_CHOICES = (
    ('pending', u'Ожидает проверки'),
    ('active', u'Активный'),
)


class Section(models.Model):
    '''
    Раздел
    '''
    title = models.CharField(
        max_length=255,
        verbose_name=u'Заголовок',
    )
    priority = models.PositiveIntegerField(
        verbose_name=u'Приоритет при показе',
        default=0,
    )
    status = models.CharField(
        verbose_name=u'Статус',
        max_length=10,
        choices=SECTION_STATUS_CHOICES,
        default='active',
    )
    version = IntegerVersionField(
        verbose_name=u'Версия'
    )
    habr_icon = models.CharField(
        max_length=255,
        verbose_name=u'Иконка для хабры',
        null=True, blank=True
    )

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['-pk']
        verbose_name = u'Раздел'
        verbose_name_plural = u'Разделы'


class Resource(models.Model):
    '''
    Источник получения информации
    '''
    title = models.CharField(
        max_length=255,
        verbose_name=u'Заголовок',
    )
    description = models.TextField(
        verbose_name=u'Описание',
        null=True, blank=True,
    )
    link = models.URLField(
        max_length=255,
        verbose_name=u'Ссылка',
    )
    version = IntegerVersionField(
        verbose_name=u'Версия'
    )

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = u'Источник'
        verbose_name_plural = u'Источники'


ITEM_STATUS_CHOICES = (
    ('pending', u'Ожидает рассмотрения'),
    ('active', u'Активная'),
    ('draft', u'Черновик'),
    ('moderated', u'Отмодерировано'),
    ('autoimport', u'Добавлена автоимпортом'),
)

ITEM_LANGUAGE_CHOICES = (
    ('ru', u'Русский'),
    ('en', u'Английский'),
)


class Item(models.Model):
    '''
    Новость
    '''
    section = models.ForeignKey(
        Section,
        verbose_name=u'Раздел',
        null=True, blank=True,
    )
    title = models.CharField(
        max_length=255,
        verbose_name=u'Заголовок',
    )
    is_editors_choice = models.BooleanField(
        verbose_name=u'Выбор редакции',
        default=False,
    )
    description = models.TextField(
        verbose_name=u'Описание',
        null=True, blank=True,
    )
    issue = models.ForeignKey(
        Issue,
        verbose_name=u'Выпуск дайджеста',
        null=True, blank=True,
    )
    resource = models.ForeignKey(
        Resource,
        verbose_name=u'Источник',
        null=True, blank=True,
    )
    link = models.URLField(
        max_length=255,
        verbose_name=u'Ссылка',
    )
    related_to_date = models.DateField(
        verbose_name=u'Дата, к которой имеет отношение новость',
        help_text=u'Например, дата публикации новости на источнике',
        default=datetime.datetime.today,
    )
    status = models.CharField(
        verbose_name=u'Статус',
        max_length=10,
        choices=ITEM_STATUS_CHOICES,
        default='pending',
    )
    language = models.CharField(
        verbose_name=u'Язык новости',
        max_length=2,
        choices=ITEM_LANGUAGE_CHOICES,
        default='en',
    )
    created_at = models.DateField(
        verbose_name=u'Дата публикации',
        auto_now_add=True,
    )
    modified_at = models.DateTimeField(
        verbose_name=u'Дата изменения',
        null=True, blank=True,
    )
    priority = models.PositiveIntegerField(
        verbose_name=u'Приоритет при показе',
        default=0,
    )
    user = models.ForeignKey(
        User,
        verbose_name=u'Кто добавил новость',
        editable=False,
        null=True, blank=True,
    )
    version = IntegerVersionField(
        verbose_name=u'Версия'
    )

    def save(self, *args, **kwargs):
        try:
            if self.issue is None:
                date_from, date_to = get_start_end_of_week(self.created_at)
                issue = Issue.objects.filter(date_from=date_from, date_to=date_to)
                assert len(issue) == 1
                self.issue = issue[0]
        except Exception as e:
            pass
        super(Item, self).save(*args, **kwargs)

    @property
    def internal_link(self):
        return reverse('frontend:item', kwargs={'pk': self.pk})

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = u'Новость'
        verbose_name_plural = u'Новости'


class AutoImportResource(models.Model):
    '''
    Источники импорта новостей
    '''
    TYPE_RESOURCE = (
        ('twitter', u'Сообщения аккаунтов в твиттере'),
        ('rss', u'RSS фид'),
    )
    
    name = models.CharField(
        max_length=255,
        verbose_name=u'Название источника',
    )
    link = models.URLField(
        max_length=255,
        verbose_name=u'Ссылка',
    )
    type_res = models.CharField(
        max_length=255,
        verbose_name=u'Тип источника',
        choices=TYPE_RESOURCE,
        default='twitter',
    )
    resource = models.ForeignKey(
        Resource,
        verbose_name=u'Источник',
        null=True, 
        blank=True,
    )
    incl = models.CharField(
        max_length=255,
        verbose_name=u'Обязательное содержание',
        help_text='Условие отбора новостей <br /> \
                   Включение вида [text] <br /> \
                   Включение при выводе будет удалено',
        null=True,
        blank=True,
    )
    excl = models.TextField(
        verbose_name=u'Список исключений',
        help_text='Список источников подлежащих исключению через ", "',
        null=True,
        blank=True,
    )
    in_edit = models.BooleanField(
        verbose_name=u'На тестировании',
        default=False,
    )

    language = models.CharField(
        verbose_name=u'Язык источника',
        max_length=2,
        choices=ITEM_LANGUAGE_CHOICES,
        default='en',
    )


    def __unicode__(self):
        return self.name


    class Meta:
        verbose_name = u'Источник импорта новостей'
        verbose_name_plural = u'Источники импорта новостей'