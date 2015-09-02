# -*- coding: utf-8 -*-
from django.db import models


class JobFeed(models.Model):
    """RSS - источники импорта вакансий."""
    name = models.CharField(
        max_length=255,
        verbose_name=u'Название источника',
    )

    link = models.URLField(
        max_length=255, verbose_name=u'Ссылка',
    )

    in_edit = models.BooleanField(
        verbose_name=u'На тестировании',
        default=False,
    )

    is_activated = models.BooleanField(verbose_name=u'Включено',
                                       default=True, )
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'Источник импорта вакансий'
        verbose_name_plural = u'Источники импорта вакансий'

class RejectedList(models.Model):
    title = models.CharField('Строка', max_length=255)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Слисок исключения'
        verbose_name_plural = 'Строки для исключения'

class AcceptedList(models.Model):
    title = models.CharField('Строка', max_length=255)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Слисок одобрения'
        verbose_name_plural = 'Строки для одобрения'

class JobItem(models.Model):
    title = models.CharField('Название', max_length=255)
    employer_name = models.CharField('Работодатель', max_length=255)
    place = models.CharField('Место', max_length=255)
    link = models.URLField('Ссылка')

    salary_from = models.PositiveIntegerField('Заработная плата', null=True,
                                              blank=True)
    salary_till = models.PositiveIntegerField('З/п до', null=True, blank=True)
    salary_currency = models.CharField('Валюта', max_length=255, null=True,
                                       blank=True)

    url_api = models.URLField('URL API', null=True, blank=True)
    url_logo = models.URLField('URL логотипа', null=True, blank=True)

    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Работа'
