# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from django.db import models

import concurrency.fields


class Migration(migrations.Migration):

    dependencies = [('digest', '0006_auto_20150113_1001'), ]

    operations = [migrations.DeleteModel(name='IssueHabr', ),
                  migrations.AlterField(
                      model_name='issue',
                      name='version',
                      field=concurrency.fields.IntegerVersionField(
                          default=0,
                          help_text='record revision number',
                          verbose_name='\u0412\u0435\u0440\u0441\u0438\u044f'),
                      preserve_default=True, ),
                  migrations.AlterField(
                      model_name='item',
                      name='version',
                      field=concurrency.fields.IntegerVersionField(
                          default=0,
                          help_text='record revision number',
                          verbose_name='\u0412\u0435\u0440\u0441\u0438\u044f'),
                      preserve_default=True, ),
                  migrations.AlterField(
                      model_name='resource',
                      name='version',
                      field=concurrency.fields.IntegerVersionField(
                          default=0,
                          help_text='record revision number',
                          verbose_name='\u0412\u0435\u0440\u0441\u0438\u044f'),
                      preserve_default=True, ),
                  migrations.AlterField(
                      model_name='section',
                      name='version',
                      field=concurrency.fields.IntegerVersionField(
                          default=0,
                          help_text='record revision number',
                          verbose_name='\u0412\u0435\u0440\u0441\u0438\u044f'),
                      preserve_default=True, ), ]
