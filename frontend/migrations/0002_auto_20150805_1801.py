# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL),
                    ('frontend', '0001_initial'), ]

    operations = [migrations.CreateModel(
        name='EditorMaterial',
        fields=[('id', models.AutoField(primary_key=True,
                                        verbose_name='ID',
                                        serialize=False,
                                        auto_created=True)),
                ('title', models.CharField(max_length=255,
                                           verbose_name='Заголовок')),
                ('slug', models.SlugField(
                    verbose_name='Идентификатор для URL')),
                ('section', models.CharField(max_length=50,
                                             choices=[('news', 'Новости'), (
                                                 'articles', 'Статьи'
                                             ), ('landing',
                                                 'Посадочные страницы')],
                                             verbose_name='Рубрика',
                                             default='landing')),
                ('status', models.CharField(max_length=50,
                                            choices=[('draft', 'Черновик'),
                                                     ('active', 'Активная'),
                                                     ('trash', 'Удалена')],
                                            verbose_name='Статус',
                                            default='draft')),
                ('announce',
                 models.TextField(max_length=1000,
                                  blank=True,
                                  verbose_name='Краткий анонс материала без разметки',
                                  null=True)),
                ('contents', models.TextField(verbose_name='Основной текст')),
                ('created_at', models.DateTimeField(auto_now_add=True,
                                                    verbose_name='Дата добавления')),
                ('user', models.ForeignKey(verbose_name='Автор',
                                           editable=False,
                                           to=settings.AUTH_USER_MODEL)), ],
        options={
            'verbose_name': 'Материал редакции',
            'verbose_name_plural': 'Материалы редакции',
        }, ),
        migrations.AlterUniqueTogether(
            name='editormaterial',
            unique_together=set([('slug', 'section')]), ), ]
