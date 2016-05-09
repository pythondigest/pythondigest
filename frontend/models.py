# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models

EDITOR_MATERIAL_SECTION_CHOICES = (('news', 'Новости'),
                                   ('articles', 'Статьи'),
                                   ('landing', 'Посадочные страницы'),)

EDITOR_MATERIAL_STATUS_CHOICES = (('draft', 'Черновик'),
                                  ('active', 'Активная'),
                                  ('trash', 'Удалена'),)


class EditorMaterial(models.Model):
    """Редкационные материалы (новости, статьи, просто страницы сайта)"""
    title = models.CharField(max_length=255, verbose_name='Заголовок', )
    slug = models.SlugField(verbose_name='Идентификатор для URL', )
    section = models.CharField(max_length=50,
                               verbose_name='Рубрика',
                               choices=EDITOR_MATERIAL_SECTION_CHOICES,
                               default='landing', )
    status = models.CharField(max_length=50,
                              verbose_name='Статус',
                              choices=EDITOR_MATERIAL_STATUS_CHOICES,
                              default='draft', )
    announce = models.TextField(
        max_length=1000,
        verbose_name='Краткий анонс материала без разметки',
        null=True,
        blank=True)
    contents = models.TextField(verbose_name='Основной текст', )
    user = models.ForeignKey(User, verbose_name='Автор', editable=False, )
    created_at = models.DateTimeField(verbose_name='Дата добавления',
                                      auto_now_add=True, )

    @property
    def link(self):
        view_kwargs = {'slug': self.slug, 'section': self.section}

        if self.section == 'landing':
            del view_kwargs['section']
            return reverse('frontend:landing', kwargs=view_kwargs)

        return reverse('frontend:editor_material', kwargs=view_kwargs)

    def __str__(self):
        return self.title

    class Meta:
        unique_together = ('slug', 'section',)
        verbose_name = 'Материал редакции'
        verbose_name_plural = 'Материалы редакции'


class Tip(models.Model):
    text = models.TextField(verbose_name='Совет')

    active = models.BooleanField(verbose_name='Активен', default=True, )

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Рекомендация'
        verbose_name_plural = 'Рекомендации'
