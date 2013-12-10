from django import forms
from digest.models import Item

class AddNewsForm(forms.ModelForm):
    class Meta:
        model = Item
        exclude = ('section', 'issue', 'resourse',
                   'related_to_date', 'status', 'resource',
                   'language', 'created_at', 'priority')

    def __init__(self, *args, **kwargs):
        super(AddNewsForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs = {'class':'form-control small form-group', 'style':'width:40%'}
        self.fields['link'].widget.attrs = {'class':'form-control small form-group', 'style':'width:40%'}
        self.fields['description'].widget.attrs = {'class':'form-control form-group', 'style':'width:40%'}
