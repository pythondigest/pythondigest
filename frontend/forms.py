from django import forms
from digest.models import Item


class AddNewsForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('link', 'section', 'title', 'description')

    def __init__(self, *args, **kwargs):
        kwargs['initial'] = {'section': 6}
        super(AddNewsForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs = {'class':'form-control small', 'style':'width:40%'}
        self.fields['title'].required = False
        self.fields['link'].widget.attrs = {'class':'form-control small', 'style':'width:40%'}
        self.fields['description'].widget.attrs = {'class':'form-control', 'style':'width:40%'}
        self.fields['section'].widget.attrs = {'class': 'form-control', 'style':'width:40%'}
