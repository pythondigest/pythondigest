from django.contrib.auth import get_user_model
from django.forms import ValidationError
from django.test import TestCase

from digest.forms import AddNewsForm, HoneypotField, HoneypotWidget
from digest.models import Section

User = get_user_model()


class HoneypotWidgetTest(TestCase):
    def test_always_rendered_as_hidden(self):
        widget = HoneypotWidget()

        self.assertTrue(widget.is_hidden)

    def test_init_if_class_in_attrs(self):
        widget = HoneypotWidget(attrs={'class': 'titanic'})

        self.assertNotIn('style', widget.attrs)
        self.assertEqual(widget.attrs['class'], 'titanic')

    def test_init_if_class_not_in_attrs(self):
        widget = HoneypotWidget(attrs={'spam': 1, 'ham': 2})

        self.assertEqual(widget.attrs['style'], 'display:none')

    def test_init_if_style_in_attrs_and_class_is_no(self):
        widget = HoneypotWidget(attrs={'style': 'float:none'})

        self.assertEqual(widget.attrs['style'], 'display:none')

    def test_render_if_html_comment_is_true(self):
        widget = HoneypotWidget(html_comment=True)

        html = widget.render('field_name', 'Field value')

        # Просто проверяем что содержимое закомментировано
        self.assertTrue(html.startswith('<!--'))
        self.assertTrue(html.endswith('-->'))

    def test_render_if_html_comment_is_false(self):
        widget = HoneypotWidget(html_comment=False)

        html = widget.render('field_name', 'Field value')

        # Нет нужды проверять всю разметку. Только наличие данных
        self.assertIn('field_name', html)
        self.assertIn('Field value', html)


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

    def test_initial_not_in_EMPTY_VALUES_and_value_is_not_equal_to_initial(self
                                                                           ):
        field = HoneypotField(initial='foobar')

        with self.assertRaises(ValidationError):
            field.clean('pizza')


# Стили виджетов не протестированы, т.к. не влияют на работоспособность формы.
class AddNewsFormTest(TestCase):
    def setUp(self):
        self.section_data = {
            'title': 'some section',
            'status': 'active',
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
            'language': 'en',
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
        # self.assertNotIn('selected', form.as_p())

    def test_form_rendering_if_6th_section_exists(self):
        Section.objects.create(pk=6, **self.section_data)

        self.section_data['title'] = 'Another title 1'
        Section.objects.create(pk=3, **self.section_data)

        self.section_data['title'] = 'Another title 2'
        Section.objects.create(pk=7, **self.section_data)

        form = AddNewsForm()

        self.assertIn(
            '<option value="6" selected="selected">some section</option>\n',
            form.as_p())
        self.assertIn('Another title 1', form.as_p())
        self.assertIn('Another title 2', form.as_p())
