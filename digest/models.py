# -*- coding: utf-8 -*-
import datetime

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext as _
from concurrency.fields import IntegerVersionField

from frontend.models import Tip

ISSUE_STATUS_CHOICES = (('active', u'Активный'), ('draft', u'Черновик'), )


def get_start_end_of_week(dt):
    start = dt - datetime.timedelta(days=dt.weekday())
    end = start + datetime.timedelta(days=6)
    return start, end


class Tag(models.Model):

    name = models.CharField(max_length=255,
                            verbose_name=u'Название тэга',
                            unique=True, )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'Тэг к новости'
        verbose_name_plural = u'Тэги к новостям'


class Issue(models.Model):

    """Выпуск дайджеста."""
    title = models.CharField(max_length=255, verbose_name=u'Заголовок', )
    description = models.TextField(verbose_name=u'Описание',
                                   null=True,
                                   blank=True, )
    image = models.ImageField(verbose_name=u'Постер',
                              upload_to='issues',
                              null=True,
                              blank=True, )
    date_from = models.DateField(verbose_name=u'Начало освещаемого периода',
                                 null=True,
                                 blank=True, )
    date_to = models.DateField(verbose_name=u'Завершение освещаемого периода',
                               null=True,
                               blank=True, )
    published_at = models.DateField(verbose_name=u'Дата публикации',
                                    null=True,
                                    blank=True, )
    status = models.CharField(verbose_name=u'Статус',
                              max_length=10,
                              choices=ISSUE_STATUS_CHOICES,
                              default='draft', )
    version = IntegerVersionField(verbose_name=u'Версия')

    tip = models.ForeignKey(Tip, null=True, blank=True, verbose_name=u'Совет')

    last_item = models.IntegerField(
        verbose_name='Последняя модерированая новость',
        blank=True,
        null=True, )

    def __str__(self):
        return self.title

    @property
    def link(self):
        return reverse('digest:issue_view', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-pk']
        verbose_name = u'Выпуск дайджеста'
        verbose_name_plural = u'Выпуски дайджеста'


SECTION_STATUS_CHOICES = (('pending', u'Ожидает проверки'),
                          ('active', u'Активный'), )


class Section(models.Model):

    """Раздел."""
    title = models.CharField(max_length=255, verbose_name=u'Заголовок', )
    priority = models.PositiveIntegerField(
        verbose_name=u'Приоритет при показе',
        default=0, )
    status = models.CharField(verbose_name=u'Статус',
                              max_length=10,
                              choices=SECTION_STATUS_CHOICES,
                              default='active', )
    version = IntegerVersionField(verbose_name=u'Версия')
    habr_icon = models.CharField(max_length=255,
                                 verbose_name=u'Иконка для хабры',
                                 null=True,
                                 blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-pk']
        verbose_name = u'Раздел'
        verbose_name_plural = u'Разделы'


class Resource(models.Model):

    """Источник получения информации."""
    title = models.CharField(max_length=255, verbose_name=u'Заголовок', )
    description = models.TextField(verbose_name=u'Описание',
                                   null=True,
                                   blank=True, )
    link = models.URLField(max_length=255, verbose_name=u'Ссылка', )
    version = IntegerVersionField(verbose_name=u'Версия')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = u'Источник'
        verbose_name_plural = u'Источники'


ITEM_STATUS_CHOICES = (
    ('pending', u'На рассмотрении'),
    ('active', u'Активная'),
    ('draft', u'Черновик'),
    ('moderated', u'Рассмотрена'),
    ('autoimport', u'Автоимпорт'),
    ('queue', u'В очереди'),
)

ITEM_LANGUAGE_CHOICES = (('ru', u'Русский'), ('en', u'Английский'), )


class Item(models.Model):

    """Новость."""
    section = models.ForeignKey(Section,
                                verbose_name=u'Раздел',
                                null=True,
                                blank=True, )
    title = models.CharField(max_length=255, verbose_name=u'Заголовок', )
    is_editors_choice = models.BooleanField(verbose_name=u'Выбор редакции',
                                            default=False, )
    description = models.TextField(verbose_name=u'Описание',
                                   null=True,
                                   blank=True, )
    issue = models.ForeignKey(Issue,
                              verbose_name=u'Выпуск дайджеста',
                              null=True,
                              blank=True, )
    resource = models.ForeignKey(Resource,
                                 verbose_name=u'Источник',
                                 null=True,
                                 blank=True, )
    link = models.URLField(max_length=255, verbose_name=u'Ссылка', )
    additionally = models.CharField(max_length=255,
                                    verbose_name=u'Дополнительно',
                                    null=True,
                                    blank=True)
    related_to_date = models.DateField(
        verbose_name=u'Дата',
        help_text=u'Например, дата публикации новости на источнике',
        default=datetime.datetime.today, )
    status = models.CharField(verbose_name=u'Статус',
                              max_length=10,
                              choices=ITEM_STATUS_CHOICES,
                              default='pending', )
    language = models.CharField(verbose_name=u'Язык новости',
                                max_length=2,
                                choices=ITEM_LANGUAGE_CHOICES,
                                default='en', )
    created_at = models.DateField(verbose_name=u'Дата публикации',
                                  auto_now_add=True, )
    modified_at = models.DateTimeField(verbose_name=u'Дата изменения',
                                       null=True,
                                       blank=True, )

    activated_at = models.DateTimeField(
        verbose_name=u'Дата активации',
        default=datetime.datetime.now,
    )
    priority = models.PositiveIntegerField(
        verbose_name=u'Приоритет при показе',
        default=0, )
    user = models.ForeignKey(User,
                             verbose_name=u'Кто добавил новость',
                             editable=False,
                             null=True,
                             blank=True, )
    version = IntegerVersionField(verbose_name=u'Версия')

    tags = models.ManyToManyField(Tag, verbose_name=u'Тэги', blank=True, )

    to_update = models.BooleanField(verbose_name=u'Обновить новость',
                                    default=False, )

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
                    raise Exception('Несколько выпусков на неделе')

        except Exception as e:
            pass
        super(Item, self).save(*args, **kwargs)

    @property
    def internal_link(self):
        return reverse('digest:item', kwargs={'pk': self.pk})

    @property
    def get_tags_str(self):
        if self.tags and self.tags.all():
            result = ','.join([x.name for x in self.tags.all()])
        else:
            result = 'Without tag'
        return result

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = u'Новость'
        verbose_name_plural = u'Новости'


class AutoImportResource(models.Model):

    """Источники импорта новостей."""
    TYPE_RESOURCE = (('twitter', u'Сообщения аккаунтов в твиттере'),
                     ('rss', u'RSS фид'), )

    name = models.CharField(max_length=255,
                            verbose_name=u'Название источника', )
    link = models.URLField(max_length=255, verbose_name=u'Ссылка', )
    type_res = models.CharField(max_length=255,
                                verbose_name=u'Тип источника',
                                choices=TYPE_RESOURCE,
                                default='twitter', )
    resource = models.ForeignKey(Resource,
                                 verbose_name=u'Источник',
                                 null=True,
                                 blank=True, )
    incl = models.CharField(max_length=255,
                            verbose_name=u'Обязательное содержание',
                            help_text='Условие отбора новостей <br /> \
                   Включение вида [text] <br /> \
                   Включение при выводе будет удалено',
                            null=True,
                            blank=True, )
    excl = models.TextField(
        verbose_name=u'Список исключений',
        help_text='Список источников подлежащих исключению через ", "',
        null=True,
        blank=True, )
    in_edit = models.BooleanField(verbose_name=u'На тестировании',
                                  default=False, )

    language = models.CharField(verbose_name=u'Язык источника',
                                max_length=2,
                                choices=ITEM_LANGUAGE_CHOICES,
                                default='en', )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'Источник импорта новостей'
        verbose_name_plural = u'Источники импорта новостей'


class Package(models.Model):

    name = models.CharField(max_length=255, verbose_name=u'Название', )

    description = models.TextField(verbose_name=u'Описание',
                                   null=True,
                                   blank=True, )

    url = models.CharField(max_length=255, verbose_name=u'Ссылка', )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'Библиотека'
        verbose_name_plural = u'Библиотеки'


class ParsingRules(models.Model):

    IF_ELEMENTS = (('title', u'Заголовок новости'), ('link', u'Url новости'),
                   ('content', u'Текст новости'),
                   ('description', u'Описание новости'),
                   ('http_code', u'HTTP Code'), )

    IF_ACTIONS = (('equal', u'Равен'), ('contains', u'Содержит'),
                  ('not_equal', u'Не равен'), ('regex', u'Regex match'), )

    THEN_ELEMENT = (('title', u'Заголовок новости'),
                    ('description', u'Описание новости'),
                    ('section', u'Раздел'), ('status', u'Статус'),
                    ('tags', u'Тэг новости'), )

    THEN_ACTION = (('set', u'Установить'), ('add', u'Добавить'),
                   ('remove', u'Удалить часть строки'), )

    name = models.CharField(max_length=255, verbose_name=u'Название правила', )

    is_activated = models.BooleanField(verbose_name=u'Включено',
                                       default=True, )

    if_element = models.CharField(max_length=255,
                                  verbose_name=u'Элемент условия',
                                  choices=IF_ELEMENTS,
                                  default='item_title', )

    if_action = models.CharField(max_length=255,
                                 verbose_name=u'Условие',
                                 choices=IF_ACTIONS,
                                 default='consist', )

    if_value = models.CharField(max_length=255, verbose_name=u'Значение', )

    then_element = models.CharField(max_length=255,
                                    verbose_name=u'Элемент действия',
                                    choices=THEN_ELEMENT,
                                    default='item_title', )

    then_action = models.CharField(max_length=255,
                                   verbose_name=u'Действие',
                                   choices=THEN_ACTION,
                                   default='item_title', )

    then_value = models.CharField(max_length=255, verbose_name=u'Значение', )

    weight = models.PositiveIntegerField(default=100, verbose_name=_('Weight'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'Правило обработки'
        verbose_name_plural = u'Правила обработки'
