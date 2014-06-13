# -*- coding: utf-8 -*-
from concurrency.fields import IntegerVersionField

from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail

from subscribe.models import Subscribers


ISSUE_STATUS_CHOICES = (
    ('active', u'Активный'),
    ('draft', u'Черновик'),
)

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
    version = IntegerVersionField()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-pk']
        verbose_name = u'Выпуск дайджеста'
        verbose_name_plural = u'Выпуски дайджеста'


SECTION_STATUS_CHOICES = (
    ('pending', u'Ожидает провери'),
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
    version = IntegerVersionField()
    habr_icon = models.CharField(
        max_length=255,
        verbose_name=u'Иконка для хабры',
        null=True, blank=True
    )

    def __str__(self):
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
    version = IntegerVersionField()

    def __str__(self):
        return self.title


    class Meta:
        verbose_name = u'Источник'
        verbose_name_plural = u'Источники'


ITEM_STATUS_CHOICES = (
    ('pending', u'Ожидает рассмотрения'),
    ('active', u'Активная'),
    ('draft', u'Черновик'),
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
    )
    status = models.CharField(
        verbose_name=u'Статус',
        max_length=10,
        choices=ITEM_STATUS_CHOICES,
        default='active',
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
    priority = models.PositiveIntegerField(
        verbose_name=u'Приоритет при показе',
        default=0,
    )
    version = IntegerVersionField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = u'Новость'
        verbose_name_plural = u'Новости'



@receiver(post_save, sender=Issue)
def send_email(sender, instance, **kwargs):

    emails = Subscribers.objects.all().values_list('useremail', flat=True)
    obj = Issue.objects.get(id=instance.id)

    if (instance.status == 'active'):
        items = obj.item_set.filter(status='active').order_by('-section__priority', '-priority')
        links = items.values_list('link', flat=True)
        for _ in links:
            print (_)
        send_mail(instance.title, instance.description,
                  "Python Digest <example@example.com>", emails)
    #NOTE
    # create html for email list
