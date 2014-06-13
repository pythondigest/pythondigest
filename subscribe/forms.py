from django import forms
from subscribe.models import Subscribers

EMPTY_VALUES = (None, '')


class HoneypotWidget(forms.TextInput):
    is_hidden = True

    def __init__(self, attrs=None, html_comment=False, *args, **kwargs):
        self.html_comment = html_comment
        super(HoneypotWidget, self).__init__(attrs, *args, **kwargs)
        if not 'class' in self.attrs:
            self.attrs['style'] = 'display:none'

    def render(self, *args, **kwargs):
        value = super(HoneypotWidget, self).render(*args, **kwargs)
        if self.html_comment:
            value = '<!-- %s -->' % value
        return value


class HoneypotField(forms.Field):
    widget = HoneypotWidget

    def clean(self, value):
        if self.initial in EMPTY_VALUES and value in EMPTY_VALUES or value == self.initial:
            return value
        raise forms.ValidationError('Anti-spam field changed in value.')


class AddSubscriber(forms.ModelForm):
    name = HoneypotField()

    class Meta:
        model = Subscribers
        fields = ('useremail',)


    def __init__(self, *args, **kwargs):
        kwargs['initial'] = {'section': 1}
        super().__init__(*args, **kwargs)
        self.fields['useremail'].widget.attrs = {'class': 'form-control small', 'style': 'width:40%'}
