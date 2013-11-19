# -*- coding: utf-8 -*-
from django.db import models
from concurrency.fields import IntegerVersionField

class ResourceRSS(models.Model):
    '''
        RSS resource model
    '''
    title = models.CharField(
        max_length=255,
        verbose_name=u'Заголовок',
    )
    description = models.TextField(
        verbose_name=u'Описание',
        null=True,
        blank=True,
    )
    link = models.URLField(
        verbose_name=u'Ссылка',
    )
    status = models.BooleanField(
        verbose_name=u'Обновлять поток',
        default=True,
    )
    sync_date = models.DateField(
        verbose_name=u'Дата синхронизации',
    )
    version = IntegerVersionField()

    def __unicode__(self):
        return self.title


    class Meta:
        verbose_name = u'Источник'
        verbose_name_plural = u'Источники'


class RawItem(models.Model):
    '''
        "Сырые" новости из RSS
    '''
    title = models.CharField(
        max_length=255,
        verbose_name=u'Заголовок',
    )
    description = models.TextField(
        verbose_name=u'Описание',
        null=True,
        blank=True,
    )
    link = models.URLField(
        verbose_name=u'Ссылка',
    )
    related_to_date = models.DateField(
        verbose_name=u'Дата новости',
    )
    version = IntegerVersionField()

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = u'Новость'
        verbose_name_plural = u'Новости'
