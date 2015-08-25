# -*- encoding: utf-8 -*-
from django.contrib import admin
from django.contrib.admin import widgets
from django.contrib.admin.options import get_ul_class
from django.forms import ChoiceField, ModelForm

from .models import Item

ITEM_STATUS_CHOICES = (('queue', u'В очередь'),
                       ('moderated', u'Отмодерировано'), )


class ItemStatusForm(ModelForm):
    status = ChoiceField(label=u"Статус",
                         widget=widgets.AdminRadioSelect(
                             attrs={'class': get_ul_class(admin.HORIZONTAL)}),
                         choices=ITEM_STATUS_CHOICES)

    class Meta:
        model = Item
        fields = '__all__'
