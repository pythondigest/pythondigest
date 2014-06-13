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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('useremail', models.EmailField(max_length=75, unique=True)),
                ('subscribe', models.BooleanField(default=True)),
                ('id_subscriber', models.CharField(max_length=50, default='9f5385332cd44a98b6cc0eae4eac4ec8', unique=True)),
            ],
            options={
                'verbose_name_plural': 'Получатели рассылки',
                'verbose_name': 'Получателя рассылки',
            },
            bases=(models.Model,),
        ),
    ]
