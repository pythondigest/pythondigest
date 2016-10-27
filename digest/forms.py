# -*- encoding: utf-8 -*-
from ckeditor.widgets import CKEditorWidget, json_encode
from django import forms
from django.contrib import admin
from django.contrib.admin import widgets
from django.contrib.admin.options import get_ul_class
from django.forms import ChoiceField, ModelForm
from django.template.loader import render_to_string
from django.utils.encoding import force_text
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

try:
    # Django >=1.7
    from django.forms.utils import flatatt
except ImportError:
    # Django <1.7
    from django.forms.util import flatatt

from digest.models import Item

ITEM_STATUS_CHOICES = (
    ('queue', 'В очередь'),
    ('moderated', 'Отмодерировано'),
)


class GlavRedWidget(CKEditorWidget):
    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, name=name)
        self._set_config()
        external_plugin_resources = [
            [force_text(a), force_text(b), force_text(c)]
            for a, b, c in self.external_plugin_resources]

        return mark_safe(
            render_to_string('custom_widget/ckeditor_widget.html', {
                'final_attrs': flatatt(final_attrs),
                'value': conditional_escape(force_text(value)),
                'id': final_attrs['id'],
                'config': json_encode(self.config),
                'external_plugin_resources': json_encode(
                    external_plugin_resources)
            }))


class ItemStatusForm(ModelForm):
    status = ChoiceField(label='Статус',
                         widget=widgets.AdminRadioSelect(
                             attrs={'class': get_ul_class(admin.HORIZONTAL)}),
                         choices=ITEM_STATUS_CHOICES)

    class Meta:
        model = Item
        fields = '__all__'
        widgets = {
            'description': GlavRedWidget,
        }


EMPTY_VALUES = (None, '')


class HoneypotWidget(forms.TextInput):
    is_hidden = True

    def __init__(self, attrs=None, html_comment=False, *args, **kwargs):
        self.html_comment = html_comment

        super(HoneypotWidget, self).__init__(attrs, *args, **kwargs)

        if 'class' not in self.attrs:
            self.attrs['style'] = 'display:none'

    def render(self, *args, **kwargs):
        html = super(HoneypotWidget, self).render(*args, **kwargs)

        if self.html_comment:
            html = '<!-- %s -->' % html

        return html


class HoneypotField(forms.Field):
    widget = HoneypotWidget

    def clean(self, value):
        if self.initial in EMPTY_VALUES and value in EMPTY_VALUES or value == self.initial:
            return value

        raise forms.ValidationError('Anti-spam field changed in value.')


class AddNewsForm(forms.ModelForm):
    name = HoneypotField()

    class Meta:
        model = Item
        fields = ('link', 'section', 'title', 'language', 'description',)

    def __init__(self, *args, **kwargs):
        kwargs['initial'] = {
            'section': 6
        }  # На форме 6й section будет помечен как selected
        super(AddNewsForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs = {
            'class': 'form-control small',
        }
        self.fields['title'].required = False
        self.fields['link'].widget.attrs = {
            'class': 'form-control small',
        }
        self.fields['language'].widget.attrs = {
            'class': 'form-control',
        }
        self.fields['description'].widget.attrs = {
            'class': 'form-control',
        }
        self.fields['section'].widget.attrs = {
            'class': 'form-control',
        }
