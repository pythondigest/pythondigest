# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

import concurrency.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL),
                    ]

    operations = [migrations.CreateModel(
        name='AutoImportResource',
        fields=[('id', models.AutoField(verbose_name='ID',
                                        serialize=False,
                                        auto_created=True,
                                        primary_key=True)),
                ('name', models.CharField(
                    max_length=255,
                    verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 \u0438\u0441\u0442\u043e\u0447\u043d\u0438\u043a\u0430')
                 ),
                ('link', models.URLField(max_length=255,
                                         verbose_name='\u0421\u0441\u044b\u043b\u043a\u0430')),
                ('type_res', models.CharField(
                    default=b'twitter',
                    max_length=255,
                    verbose_name='\u0422\u0438\u043f \u0438\u0441\u0442\u043e\u0447\u043d\u0438\u043a\u0430',
                    choices=[(
                        b'twitter',
                        '\u0421\u043e\u043e\u0431\u0449\u0435\u043d\u0438\u044f \u0430\u043a\u043a\u0430\u0443\u043d\u0442\u043e\u0432 \u0432 \u0442\u0432\u0438\u0442\u0442\u0435\u0440\u0435'
                    ), (b'rss', 'RSS \u0444\u0438\u0434')])),
                ('incl', models.CharField(
                    help_text=b'\xd0\xa3\xd1\x81\xd0\xbb\xd0\xbe\xd0\xb2\xd0\xb8\xd0\xb5 \xd0\xbe\xd1\x82\xd0\xb1\xd0\xbe\xd1\x80\xd0\xb0 \xd0\xbd\xd0\xbe\xd0\xb2\xd0\xbe\xd1\x81\xd1\x82\xd0\xb5\xd0\xb9 <br />             \xd0\x92\xd0\xba\xd0\xbb\xd1\x8e\xd1\x87\xd0\xb5\xd0\xbd\xd0\xb8\xd0\xb5 \xd0\xb2\xd0\xb8\xd0\xb4\xd0\xb0 [text] <br />             \xd0\x92\xd0\xba\xd0\xbb\xd1\x8e\xd1\x87\xd0\xb5\xd0\xbd\xd0\xb8\xd0\xb5 \xd0\xbf\xd1\x80\xd0\xb8 \xd0\xb2\xd1\x8b\xd0\xb2\xd0\xbe\xd0\xb4\xd0\xb5 \xd0\xb1\xd1\x83\xd0\xb4\xd0\xb5\xd1\x82 \xd1\x83\xd0\xb4\xd0\xb0\xd0\xbb\xd0\xb5\xd0\xbd\xd0\xbe',
                    max_length=255,
                    null=True,
                    verbose_name='\u041e\u0431\u044f\u0437\u0430\u0442\u0435\u043b\u044c\u043d\u043e\u0435 \u0441\u043e\u0434\u0435\u0440\u0436\u0430\u043d\u0438\u0435',
                    blank=True)),
                ('excl', models.TextField(
                    help_text=b'\xd0\xa1\xd0\xbf\xd0\xb8\xd1\x81\xd0\xbe\xd0\xba \xd0\xb8\xd1\x81\xd1\x82\xd0\xbe\xd1\x87\xd0\xbd\xd0\xb8\xd0\xba\xd0\xbe\xd0\xb2 \xd0\xbf\xd0\xbe\xd0\xb4\xd0\xbb\xd0\xb5\xd0\xb6\xd0\xb0\xd1\x89\xd0\xb8\xd1\x85 \xd0\xb8\xd1\x81\xd0\xba\xd0\xbb\xd1\x8e\xd1\x87\xd0\xb5\xd0\xbd\xd0\xb8\xd1\x8e \xd1\x87\xd0\xb5\xd1\x80\xd0\xb5\xd0\xb7 ", "',
                    null=True,
                    verbose_name='\u0421\u043f\u0438\u0441\u043e\u043a \u0438\u0441\u043a\u043b\u044e\u0447\u0435\u043d\u0438\u0439',
                    blank=True)),
                ('in_edit', models.BooleanField(
                    default=False,
                    verbose_name='\u041d\u0430 \u0442\u0435\u0441\u0442\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u0438')
                 ), ],
        options={
            'verbose_name':
                '\u0418\u0441\u0442\u043e\u0447\u043d\u0438\u043a \u0438\u043c\u043f\u043e\u0440\u0442\u0430 \u043d\u043e\u0432\u043e\u0441\u0442\u0435\u0439',
            'verbose_name_plural':
                '\u0418\u0441\u0442\u043e\u0447\u043d\u0438\u043a\u0438 \u0438\u043c\u043f\u043e\u0440\u0442\u0430 \u043d\u043e\u0432\u043e\u0441\u0442\u0435\u0439',
        },
        bases=(models.Model,), ),
        migrations.CreateModel(
            name='Issue',
            fields=[('id', models.AutoField(verbose_name='ID',
                                            serialize=False,
                                            auto_created=True,
                                            primary_key=True)),
                    ('title', models.CharField(
                        max_length=255,
                        verbose_name='\u0417\u0430\u0433\u043e\u043b\u043e\u0432\u043e\u043a')
                     ),
                    ('description', models.TextField(
                        null=True,
                        verbose_name='\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435',
                        blank=True)),
                    ('image', models.ImageField(
                        upload_to=b'issues',
                        null=True,
                        verbose_name='\u041f\u043e\u0441\u0442\u0435\u0440',
                        blank=True)),
                    ('date_from', models.DateField(
                        null=True,
                        verbose_name='\u041d\u0430\u0447\u0430\u043b\u043e \u043e\u0441\u0432\u0435\u0449\u0430\u0435\u043c\u043e\u0433\u043e \u043f\u0435\u0440\u0438\u043e\u0434\u0430',
                        blank=True)),
                    ('date_to', models.DateField(
                        null=True,
                        verbose_name='\u0417\u0430\u0432\u0435\u0440\u0448\u0435\u043d\u0438\u0435 \u043e\u0441\u0432\u0435\u0449\u0430\u0435\u043c\u043e\u0433\u043e \u043f\u0435\u0440\u0438\u043e\u0434\u0430',
                        blank=True)),
                    ('published_at', models.DateField(
                        null=True,
                        verbose_name='\u0414\u0430\u0442\u0430 \u043f\u0443\u0431\u043b\u0438\u043a\u0430\u0446\u0438\u0438',
                        blank=True)),
                    ('status', models.CharField(
                        default=b'draft',
                        max_length=10,
                        verbose_name='\u0421\u0442\u0430\u0442\u0443\u0441',
                        choices=[(b'active',
                                  '\u0410\u043a\u0442\u0438\u0432\u043d\u044b\u0439'),
                                 (b'draft',
                                  '\u0427\u0435\u0440\u043d\u043e\u0432\u0438\u043a')])),
                    ('version', concurrency.fields.IntegerVersionField(
                        default=1,
                        help_text='record revision number')), ],
            options={
                'ordering': ['-pk'],
                'verbose_name':
                    '\u0412\u044b\u043f\u0443\u0441\u043a \u0434\u0430\u0439\u0434\u0436\u0435\u0441\u0442\u0430',
                'verbose_name_plural':
                    '\u0412\u044b\u043f\u0443\u0441\u043a\u0438 \u0434\u0430\u0439\u0434\u0436\u0435\u0441\u0442\u0430',
            },
            bases=(models.Model,), ),
        migrations.CreateModel(
            name='Item',
            fields=[('id', models.AutoField(verbose_name='ID',
                                            serialize=False,
                                            auto_created=True,
                                            primary_key=True)),
                    ('title', models.CharField(
                        max_length=255,
                        verbose_name='\u0417\u0430\u0433\u043e\u043b\u043e\u0432\u043e\u043a')
                     ),
                    ('is_editors_choice', models.BooleanField(
                        default=False,
                        verbose_name='\u0412\u044b\u0431\u043e\u0440 \u0440\u0435\u0434\u0430\u043a\u0446\u0438\u0438')
                     ),
                    ('description', models.TextField(
                        null=True,
                        verbose_name='\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435',
                        blank=True)),
                    ('link', models.URLField(
                        max_length=255,
                        verbose_name='\u0421\u0441\u044b\u043b\u043a\u0430')),
                    ('related_to_date', models.DateField(
                        default=datetime.datetime.today,
                        help_text='\u041d\u0430\u043f\u0440\u0438\u043c\u0435\u0440, \u0434\u0430\u0442\u0430 \u043f\u0443\u0431\u043b\u0438\u043a\u0430\u0446\u0438\u0438 \u043d\u043e\u0432\u043e\u0441\u0442\u0438 \u043d\u0430 \u0438\u0441\u0442\u043e\u0447\u043d\u0438\u043a\u0435',
                        verbose_name='\u0414\u0430\u0442\u0430, \u043a \u043a\u043e\u0442\u043e\u0440\u043e\u0439 \u0438\u043c\u0435\u0435\u0442 \u043e\u0442\u043d\u043e\u0448\u0435\u043d\u0438\u0435 \u043d\u043e\u0432\u043e\u0441\u0442\u044c')
                     ),
                    ('status', models.CharField(
                        default=b'pending',
                        max_length=10,
                        verbose_name='\u0421\u0442\u0430\u0442\u0443\u0441',
                        choices=[(
                            b'pending',
                            '\u041e\u0436\u0438\u0434\u0430\u0435\u0442 \u0440\u0430\u0441\u0441\u043c\u043e\u0442\u0440\u0435\u043d\u0438\u044f'
                        ), (
                            b'active',
                            '\u0410\u043a\u0442\u0438\u0432\u043d\u0430\u044f'
                        ), (b'draft',
                            '\u0427\u0435\u0440\u043d\u043e\u0432\u0438\u043a'),
                            (
                                b'autoimport',
                                '\u0414\u043e\u0431\u0430\u0432\u043b\u0435\u043d\u0430 \u0430\u0432\u0442\u043e\u0438\u043c\u043f\u043e\u0440\u0442\u043e\u043c'
                            )])),
                    ('language', models.CharField(
                        default=b'en',
                        max_length=2,
                        verbose_name='\u042f\u0437\u044b\u043a \u043d\u043e\u0432\u043e\u0441\u0442\u0438',
                        choices=[(b'ru',
                                  '\u0420\u0443\u0441\u0441\u043a\u0438\u0439'),
                                 (
                                     b'en',
                                     '\u0410\u043d\u0433\u043b\u0438\u0439\u0441\u043a\u0438\u0439'
                                 )])),
                    ('created_at', models.DateField(
                        auto_now_add=True,
                        verbose_name='\u0414\u0430\u0442\u0430 \u043f\u0443\u0431\u043b\u0438\u043a\u0430\u0446\u0438\u0438')
                     ),
                    ('priority', models.PositiveIntegerField(
                        default=0,
                        verbose_name='\u041f\u0440\u0438\u043e\u0440\u0438\u0442\u0435\u0442 \u043f\u0440\u0438 \u043f\u043e\u043a\u0430\u0437\u0435')
                     ),
                    ('version', concurrency.fields.IntegerVersionField(
                        default=1,
                        help_text='record revision number')),
                    ('issue', models.ForeignKey(
                        verbose_name='\u0412\u044b\u043f\u0443\u0441\u043a \u0434\u0430\u0439\u0434\u0436\u0435\u0441\u0442\u0430',
                        blank=True,
                        on_delete=models.CASCADE,
                        to='digest.Issue',
                        null=True)), ],
            options={
                'verbose_name':
                    '\u041d\u043e\u0432\u043e\u0441\u0442\u044c',
                'verbose_name_plural':
                    '\u041d\u043e\u0432\u043e\u0441\u0442\u0438',
            },
            bases=(models.Model,), ),
        migrations.CreateModel(
            name='Resource',
            fields=[('id', models.AutoField(verbose_name='ID',
                                            serialize=False,
                                            auto_created=True,
                                            primary_key=True)),
                    ('title', models.CharField(
                        max_length=255,
                        verbose_name='\u0417\u0430\u0433\u043e\u043b\u043e\u0432\u043e\u043a')
                     ),
                    ('description', models.TextField(
                        null=True,
                        verbose_name='\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435',
                        blank=True)),
                    ('link', models.URLField(
                        max_length=255,
                        verbose_name='\u0421\u0441\u044b\u043b\u043a\u0430')),
                    ('version', concurrency.fields.IntegerVersionField(
                        default=1,
                        help_text='record revision number')), ],
            options={
                'verbose_name':
                    '\u0418\u0441\u0442\u043e\u0447\u043d\u0438\u043a',
                'verbose_name_plural':
                    '\u0418\u0441\u0442\u043e\u0447\u043d\u0438\u043a\u0438',
            },
            bases=(models.Model,), ),
        migrations.CreateModel(
            name='Section',
            fields=[('id', models.AutoField(verbose_name='ID',
                                            serialize=False,
                                            auto_created=True,
                                            primary_key=True)),
                    ('title', models.CharField(
                        max_length=255,
                        verbose_name='\u0417\u0430\u0433\u043e\u043b\u043e\u0432\u043e\u043a')
                     ),
                    ('priority', models.PositiveIntegerField(
                        default=0,
                        verbose_name='\u041f\u0440\u0438\u043e\u0440\u0438\u0442\u0435\u0442 \u043f\u0440\u0438 \u043f\u043e\u043a\u0430\u0437\u0435')
                     ),
                    ('status', models.CharField(
                        default=b'active',
                        max_length=10,
                        verbose_name='\u0421\u0442\u0430\u0442\u0443\u0441',
                        choices=[(
                            b'pending',
                            '\u041e\u0436\u0438\u0434\u0430\u0435\u0442 \u043f\u0440\u043e\u0432\u0435\u0440\u0438'
                        ), (
                            b'active',
                            '\u0410\u043a\u0442\u0438\u0432\u043d\u044b\u0439'
                        )])),
                    ('version', concurrency.fields.IntegerVersionField(
                        default=1,
                        help_text='record revision number')),
                    ('habr_icon', models.CharField(
                        max_length=255,
                        null=True,
                        verbose_name='\u0418\u043a\u043e\u043d\u043a\u0430 \u0434\u043b\u044f \u0445\u0430\u0431\u0440\u044b',
                        blank=True)), ],
            options={
                'ordering': ['-pk'],
                'verbose_name': '\u0420\u0430\u0437\u0434\u0435\u043b',
                'verbose_name_plural':
                    '\u0420\u0430\u0437\u0434\u0435\u043b\u044b',
            },
            bases=(models.Model,), ),
        migrations.AddField(
            model_name='item',
            name='resource',
            field=models.ForeignKey(
                verbose_name='\u0418\u0441\u0442\u043e\u0447\u043d\u0438\u043a',
                blank=True,
                to='digest.Resource',
                on_delete=models.CASCADE,
                null=True),
            preserve_default=True, ),
        migrations.AddField(
            model_name='item',
            name='section',
            field=models.ForeignKey(
                verbose_name='\u0420\u0430\u0437\u0434\u0435\u043b',
                blank=True,
                to='digest.Section', on_delete=models.CASCADE,
                null=True),
            preserve_default=True, ),
        migrations.AddField(
            model_name='item',
            name='user',
            field=models.ForeignKey(
                blank=True,
                editable=False,
                to=settings.AUTH_USER_MODEL,
                on_delete=models.CASCADE,
                null=True,
                verbose_name='\u041a\u0442\u043e \u0434\u043e\u0431\u0430\u0432\u0438\u043b \u043d\u043e\u0432\u043e\u0441\u0442\u044c'),
            preserve_default=True, ),
        migrations.AddField(
            model_name='autoimportresource',
            name='resource',
            field=models.ForeignKey(
                verbose_name='\u0418\u0441\u0442\u043e\u0447\u043d\u0438\u043a',
                blank=True,
                to='digest.Resource', on_delete=models.CASCADE,
                null=True),
            preserve_default=True, ), ]
