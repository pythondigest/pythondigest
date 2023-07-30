from ckeditor.widgets import CKEditorWidget
from django import forms
from django.contrib import admin
from django.contrib.admin import widgets
from django.contrib.admin.options import get_ul_class
from django.forms import ChoiceField, ModelForm

from digest.models import Item

ITEM_STATUS_DEFAULT = "queue"
ITEM_STATUS_CHOICES = (
    ("queue", "В очередь"),
    ("moderated", "Отмодерировано"),
)


class ItemStatusForm(ModelForm):
    status = ChoiceField(
        label="Статус",
        widget=widgets.AdminRadioSelect(attrs={"class": get_ul_class(admin.HORIZONTAL)}),
        choices=ITEM_STATUS_CHOICES,
    )

    class Meta:
        model = Item
        fields = "__all__"
        widgets = {
            "description": CKEditorWidget,
        }


EMPTY_VALUES = (None, "")


class HoneypotWidget(forms.TextInput):
    is_hidden = True

    def __init__(self, attrs=None, html_comment=False, *args, **kwargs):
        self.html_comment = html_comment

        super().__init__(attrs, *args, **kwargs)

        if "class" not in self.attrs:
            self.attrs["style"] = "display:none"

    def render(self, *args, **kwargs):
        html = super().render(*args, **kwargs)

        if self.html_comment:
            html = "<!-- %s -->" % html

        return html


class HoneypotField(forms.Field):
    widget = HoneypotWidget

    def clean(self, value):
        if self.initial in EMPTY_VALUES and value in EMPTY_VALUES or value == self.initial:
            return value

        raise forms.ValidationError("Anti-spam field changed in value.")


class AddNewsForm(forms.ModelForm):
    name = HoneypotField()

    class Meta:
        model = Item
        fields = (
            "link",
            "section",
            "title",
            "language",
            "description",
        )

    def __init__(self, *args, **kwargs):
        kwargs["initial"] = {"section": 6}  # На форме 6й section будет помечен как selected
        super().__init__(*args, **kwargs)
        self.fields["title"].widget.attrs = {
            "class": "form-control small",
        }
        self.fields["title"].required = False
        self.fields["link"].widget.attrs = {
            "class": "form-control small",
        }
        self.fields["language"].widget.attrs = {
            "class": "form-control",
        }
        self.fields["description"].widget.attrs = {
            "class": "form-control",
        }
        self.fields["section"].widget.attrs = {
            "class": "form-control",
        }
