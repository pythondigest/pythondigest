# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models

EDITOR_MATERIAL_SECTION_CHOICES = (('news', u'Новости'),
                                   ('articles', u'Статьи'),
                                   ('landing', u'Посадочные страницы'), )

EDITOR_MATERIAL_STATUS_CHOICES = (('draft', u'Черновик'),
                                  ('active', u'Активная'),
                                  ('trash', u'Удалена'), )


class EditorMaterial(models.Model):

    """Редкационные материалы (новости, статьи, просто страницы сайта)"""
    title = models.CharField(max_length=255, verbose_name=u'Заголовок', )
    slug = models.SlugField(verbose_name=u'Идентификатор для URL', )
    section = models.CharField(max_length=50,
                               verbose_name=u'Рубрика',
                               choices=EDITOR_MATERIAL_SECTION_CHOICES,
                               default='landing', )
    status = models.CharField(max_length=50,
                              verbose_name=u'Статус',
                              choices=EDITOR_MATERIAL_STATUS_CHOICES,
                              default='draft', )
    announce = models.TextField(
        max_length=1000,
        verbose_name=u'Краткий анонс материала без разметки',
        null=True,
        blank=True)
    contents = models.TextField(verbose_name=u'Основной текст', )
    user = models.ForeignKey(User, verbose_name=u'Автор', editable=False, )
    created_at = models.DateTimeField(verbose_name=u'Дата добавления',
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
        unique_together = ('slug', 'section', )
        verbose_name = u'Материал редакции'
        verbose_name_plural = u'Материалы редакции'


class Tip(models.Model):

    text = models.TextField(verbose_name=u'Совет')

    active = models.BooleanField(verbose_name=u'Активен', default=True, )

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = u'Рекомендация'
        verbose_name_plural = u'Рекомендации'
