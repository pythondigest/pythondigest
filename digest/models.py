# -*- coding: utf-8 -*-
from sleekxmpp import ClientXMPP
from concurrency.fields import IntegerVersionField

from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

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

    def __unicode__(self):
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
    version = IntegerVersionField()

    def __unicode__(self):
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

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = u'Новость'
        verbose_name_plural = u'Новости'


#@receiver(post_save, sender=Item)
#def send_item(instance, **kwargs):
#    '''
#    По событию сохранения активной новости отправляет ее в juick
#    А тот в свою очередь репостит в twitter
#    '''
#    if instance.status == 'active':
#        mess = u'%s %s %s %s' % (
#            settings.JUICK_TAGS,
#            instance.title,
#            instance.link,
#            instance.description
#        )
#        xmpp = ClientXMPP(
#            settings.JABBER_USER,
#            settings.JABBER_PASS
#        )
#        xmpp.connect()

#        def on_start(e):
#            xmpp.send_message(mto='juick@juick.com', mbody=mess, mtype='chat')
#            xmpp.disconnect(wait=True)
#        xmpp.add_event_handler('session_start', on_start)
#        xmpp.process()
