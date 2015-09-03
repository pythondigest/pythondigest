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

    is_activated = models.BooleanField(
        verbose_name=u'Включено',
        default=True,
    )

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
    link = models.URLField('Ссылка')
    description = models.TextField(
        'Описание вакансии',
        null=True,
        blank=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Работа'
