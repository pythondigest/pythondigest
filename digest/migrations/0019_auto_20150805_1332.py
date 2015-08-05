# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('digest', '0018_package'),
    ]

    operations = [
        migrations.AlterField(
            model_name='autoimportresource',
            name='excl',
            field=models.TextField(blank=True, verbose_name='Список исключений', help_text='Список источников подлежащих исключению через ", "', null=True),
        ),
        migrations.AlterField(
            model_name='autoimportresource',
            name='incl',
            field=models.CharField(blank=True, verbose_name='Обязательное содержание', max_length=255, help_text='Условие отбора новостей <br />                    Включение вида [text] <br />                    Включение при выводе будет удалено', null=True),
        ),
        migrations.AlterField(
            model_name='autoimportresource',
            name='language',
            field=models.CharField(verbose_name='Язык источника', max_length=2, default='en', choices=[('ru', 'Русский'), ('en', 'Английский')]),
        ),
        migrations.AlterField(
            model_name='autoimportresource',
            name='type_res',
            field=models.CharField(verbose_name='Тип источника', max_length=255, default='twitter', choices=[('twitter', 'Сообщения аккаунтов в твиттере'), ('rss', 'RSS фид')]),
        ),
        migrations.AlterField(
            model_name='issue',
            name='image',
            field=models.ImageField(blank=True, verbose_name='Постер', upload_to='issues', null=True),
        ),
        migrations.AlterField(
            model_name='issue',
            name='status',
            field=models.CharField(verbose_name='Статус', max_length=10, default='draft', choices=[('active', 'Активный'), ('draft', 'Черновик')]),
        ),
        migrations.AlterField(
            model_name='item',
            name='language',
            field=models.CharField(verbose_name='Язык новости', max_length=2, default='en', choices=[('ru', 'Русский'), ('en', 'Английский')]),
        ),
        migrations.AlterField(
            model_name='item',
            name='status',
            field=models.CharField(verbose_name='Статус', max_length=10, default='pending', choices=[('pending', 'Ожидает рассмотрения'), ('active', 'Активная'), ('draft', 'Черновик'), ('moderated', 'Отмодерировано'), ('autoimport', 'Добавлена автоимпортом')]),
        ),
        migrations.AlterField(
            model_name='parsingrules',
            name='if_action',
            field=models.CharField(verbose_name='Условие', max_length=255, default='consist', choices=[('equal', 'Равен'), ('contains', 'Содержит'), ('not_equal', 'Не равен'), ('regex', 'Regex match')]),
        ),
        migrations.AlterField(
            model_name='parsingrules',
            name='if_element',
            field=models.CharField(verbose_name='Элемент условия', max_length=255, default='item_title', choices=[('title', 'Заголовок новости'), ('url', 'Url новости'), ('content', 'Текст новости'), ('description', 'Описание новости'), ('http_code', 'HTTP Code')]),
        ),
        migrations.AlterField(
            model_name='parsingrules',
            name='then_action',
            field=models.CharField(verbose_name='Действие', max_length=255, default='item_title', choices=[('set', 'Установить'), ('add', 'Добавить'), ('remove', 'Удалить часть строки')]),
        ),
        migrations.AlterField(
            model_name='parsingrules',
            name='then_element',
            field=models.CharField(verbose_name='Элемент действия', max_length=255, default='item_title', choices=[('title', 'Заголовок новости'), ('section', 'Раздел'), ('status', 'Статус'), ('tags', 'Тэг новости')]),
        ),
        migrations.AlterField(
            model_name='section',
            name='status',
            field=models.CharField(verbose_name='Статус', max_length=10, default='active', choices=[('pending', 'Ожидает проверки'), ('active', 'Активный')]),
        ),
    ]
