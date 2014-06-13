# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Subscribers',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('useremail', models.EmailField(max_length=75, unique=True)),
                ('subscribe', models.BooleanField(default=True)),
                ('subscriber_add', models.DateField(auto_now_add=True, verbose_name='Дата добавления')),
                ('id_subscriber', models.CharField(max_length=50, unique=True, default='41ebd1c339c5440aa998f42f6de799d4')),
            ],
            options={
                'verbose_name': 'Получателя рассылки',
                'verbose_name_plural': 'Получатели рассылки',
            },
            bases=(models.Model,),
        ),
    ]
