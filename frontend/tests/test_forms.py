from django.test import TestCase
from django.contrib.auth import get_user_model
from django.forms import ValidationError
User = get_user_model()

from digest.models import Item, Section
from frontend.models import EditorMaterial, Tip
from frontend.forms import HoneypotWidget, HoneypotField, AddNewsForm


class HoneypotFieldTest(TestCase):

    def test_class_of_widget(self):

        field = HoneypotField()

        self.assertIsInstance(field.widget, HoneypotWidget)

    def test_initial_and_value_in_EMPTY_VALUES(self):

        field = HoneypotField(initial=None)

        output = field.clean('')

        self.assertEqual(output, '')

    def test_initial_not_in_EMPTY_VALUES_and_value_is_equal_to_initial(self):

        field = HoneypotField(initial='foobar')

        output = field.clean('foobar')

        self.assertEqual(output, 'foobar')

    def test_initial_not_in_EMPTY_VALUES_and_value_is_not_equal_to_initial(self):

        field = HoneypotField(initial='foobar')

        with self.assertRaises(ValidationError):
            field.clean('pizza')


# Стили виджетов не протестированы, т.к. не влияют на работоспособность формы.
class AddNewsFormTest(TestCase):

    def setUp(self):

        self.section_data = {
            'title': 'some section',
            'status': 'active',
            'version': '1',
        }

    def test_name_field_is_HoneypotField(self):

        form = AddNewsForm()

        self.assertIsInstance(form.fields['name'], HoneypotField)

    def test_form_save_with_valid_data(self):

        section = Section.objects.create(pk=1, **self.section_data)

        data = {
            'link': 'http://google.com',
            'title': 'hello',
            'description': 'hello world',
            'section': section.pk,
        }

        form = AddNewsForm(data)

        self.assertTrue(form.is_valid())

    def test_the_title_field_is_not_required(self):

        form = AddNewsForm()

        self.assertEqual(form.fields['title'].required, False)

    def test_form_rendering_if_no_section_exists(self):

        self.section_data['title'] = 'Another title 1'
        Section.objects.create(pk=3, **self.section_data)

        self.section_data['title'] = 'Another title 2'
        Section.objects.create(pk=7, **self.section_data)

        form = AddNewsForm()

        self.assertIn('Another title 1', form.as_p())
        self.assertIn('Another title 2', form.as_p())
        self.assertNotIn('selected', form.as_p())

    def test_form_rendering_if_6th_section_exists(self):

        Section.objects.create(pk=6, **self.section_data)

        self.section_data['title'] = 'Another title 1'
        Section.objects.create(pk=3, **self.section_data)

        self.section_data['title'] = 'Another title 2'
        Section.objects.create(pk=7, **self.section_data)

        form = AddNewsForm()

        self.assertIn('<option value="6" selected="selected">some section</option>\n', form.as_p())
        self.assertIn('Another title 1', form.as_p())
        self.assertIn('Another title 2', form.as_p())
