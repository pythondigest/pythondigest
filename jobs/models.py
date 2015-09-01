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

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'Источник импорта вакансий'
        verbose_name_plural = u'Источники импорта вакансий'
