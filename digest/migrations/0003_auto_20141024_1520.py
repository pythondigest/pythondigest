# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [('digest', '0002_auto_20140904_0901'), ]

    operations = [migrations.CreateModel(
        name='IssueHabr',
        fields=[('id', models.AutoField(verbose_name='ID',
                                        serialize=False,
                                        auto_created=True,
                                        primary_key=True)),
                ('title', models.CharField(
                    max_length=255,
                    verbose_name='\u0417\u0430\u0433\u043e\u043b\u043e\u0432\u043e\u043a')),
                ('description', models.TextField(
                    null=True,
                    verbose_name='\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435',
                    blank=True)),
                ('image', models.ImageField(upload_to=b'issues',
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
                ('version', models.BigIntegerField(
                    default=1,
                    help_text='record revision number')), ],
        options={
            'ordering': ['-pk'],
            'verbose_name':
                '\u0425\u0430\u0431\u0440\u0430\u0434\u0430\u0439\u0434\u0436\u0435\u0441\u0442',
            'verbose_name_plural':
                '\u0425\u0430\u0431\u0440\u0430\u0434\u0430\u0439\u0434\u0436\u0435\u0441\u0442\u044b',
        },
        bases=(models.Model,), ),
        migrations.RemoveField(model_name='filteringrule',
                               name='resource', ),
        migrations.DeleteModel(name='FilteringRule', ),
        migrations.AddField(
            model_name='autoimportresource',
            name='excl',
            field=models.TextField(
                help_text=b'\xd0\xa1\xd0\xbf\xd0\xb8\xd1\x81\xd0\xbe\xd0\xba \xd0\xb8\xd1\x81\xd1\x82\xd0\xbe\xd1\x87\xd0\xbd\xd0\xb8\xd0\xba\xd0\xbe\xd0\xb2 \xd0\xbf\xd0\xbe\xd0\xb4\xd0\xbb\xd0\xb5\xd0\xb6\xd0\xb0\xd1\x89\xd0\xb8\xd1\x85 \xd0\xb8\xd1\x81\xd0\xba\xd0\xbb\xd1\x8e\xd1\x87\xd0\xb5\xd0\xbd\xd0\xb8\xd1\x8e \xd1\x87\xd0\xb5\xd1\x80\xd0\xb5\xd0\xb7 ", "',
                null=True,
                verbose_name='\u0421\u043f\u0438\u0441\u043e\u043a \u0438\u0441\u043a\u043b\u044e\u0447\u0435\u043d\u0438\u0439',
                blank=True),
            preserve_default=True, ),
        migrations.AddField(
            model_name='autoimportresource',
            name='incl',
            field=models.CharField(
                help_text=b'\xd0\xa3\xd1\x81\xd0\xbb\xd0\xbe\xd0\xb2\xd0\xb8\xd0\xb5 \xd0\xbe\xd1\x82\xd0\xb1\xd0\xbe\xd1\x80\xd0\xb0 \xd0\xbd\xd0\xbe\xd0\xb2\xd0\xbe\xd1\x81\xd1\x82\xd0\xb5\xd0\xb9 <br />                    \xd0\x92\xd0\xba\xd0\xbb\xd1\x8e\xd1\x87\xd0\xb5\xd0\xbd\xd0\xb8\xd0\xb5 \xd0\xb2\xd0\xb8\xd0\xb4\xd0\xb0 [text] <br />                    \xd0\x92\xd0\xba\xd0\xbb\xd1\x8e\xd1\x87\xd0\xb5\xd0\xbd\xd0\xb8\xd0\xb5 \xd0\xbf\xd1\x80\xd0\xb8 \xd0\xb2\xd1\x8b\xd0\xb2\xd0\xbe\xd0\xb4\xd0\xb5 \xd0\xb1\xd1\x83\xd0\xb4\xd0\xb5\xd1\x82 \xd1\x83\xd0\xb4\xd0\xb0\xd0\xbb\xd0\xb5\xd0\xbd\xd0\xbe',
                max_length=255,
                null=True,
                verbose_name='\u041e\u0431\u044f\u0437\u0430\u0442\u0435\u043b\u044c\u043d\u043e\u0435 \u0441\u043e\u0434\u0435\u0440\u0436\u0430\u043d\u0438\u0435',
                blank=True),
            preserve_default=True, ),
        migrations.AlterField(
            model_name='section',
            name='status',
            field=models.CharField(
                default=b'active',
                max_length=10,
                verbose_name='\u0421\u0442\u0430\u0442\u0443\u0441',
                choices=[(
                    b'pending',
                    '\u041e\u0436\u0438\u0434\u0430\u0435\u0442 \u043f\u0440\u043e\u0432\u0435\u0440\u043a\u0438'
                ), (
                    b'active',
                    '\u0410\u043a\u0442\u0438\u0432\u043d\u044b\u0439'
                )]), ), ]
