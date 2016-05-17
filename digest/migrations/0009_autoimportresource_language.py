# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [('digest', '0008_auto_20150724_0738'), ]

    operations = [migrations.AddField(
        model_name='autoimportresource',
        name='language',
        field=models.CharField(
            default=b'en',
            max_length=2,
            verbose_name='\u042f\u0437\u044b\u043a \u0438\u0441\u0442\u043e\u0447\u043d\u0438\u043a\u0430',
            choices=[(b'ru', '\u0420\u0443\u0441\u0441\u043a\u0438\u0439'), (
                b'en',
                '\u0410\u043d\u0433\u043b\u0438\u0439\u0441\u043a\u0438\u0439'
            )]), ), ]
