from django.core.exceptions import ImproperlyConfigured
from django.db import connection
from django.forms.models import ModelChoiceIterator
from django.forms.widgets import (CheckboxSelectMultiple, RadioSelect, Select,
                                  SelectMultiple)
from django.utils.translation import gettext_lazy as _
from wagtail.admin.panels import FieldPanel
from wagtail.models import Locale


class LocalizedSelectPanel(FieldPanel):
    """
    Customised FieldPanel to filter choices based on locale of page/model being created/edited
    Usage: 
    widget_class - optional, override field widget type
                 - should be CheckboxSelectMultiple, RadioSelect, Select or SelectMultiple
    typed_choice_field - set to True with Select widget forces drop down list 
    """

    def __init__(self, field_name, widget_class=None, typed_choice_field=False, *args, **kwargs):
        if not widget_class in [None, CheckboxSelectMultiple, RadioSelect, Select, SelectMultiple]:
            raise ImproperlyConfigured(_(
                "widget_class should be a Django form widget class of type "
                "CheckboxSelectMultiple, RadioSelect, Select or SelectMultiple"
            ))
        self.widget_class = widget_class
        self.typed_choice_field = typed_choice_field
        super().__init__(field_name, *args, **kwargs)

    def clone_kwargs(self):
        return {
            'heading': self.heading,
            'classname': self.classname,
            'help_text': self.help_text,
            'widget_class': self.widget_class,
            'typed_choice_field': self.typed_choice_field,
            'field_name': self.field_name,
        }

    class BoundPanel(FieldPanel.BoundPanel): 
        def __init__(self, **kwargs):
            super().__init__(**kwargs)           
            if not self.panel.widget_class:
                self.form.fields[self.field_name].widget.choices=self.choice_list
            else:
                self.form.fields[self.field_name].widget = self.panel.widget_class(choices=self.choice_list)
            if self.panel.typed_choice_field:
                self.form.fields[self.field_name].__class__.__name__ = 'typed_choice_field'
            pass

        @property
        def choice_list(self):
            self.form.fields[self.field_name].queryset = self.form.fields[self.field_name].queryset.filter(locale_id=self.instance.locale_id)
            choices = ModelChoiceIterator(self.form.fields[self.field_name])
            return choices
        
class RegexPanel(FieldPanel):

    def __init__(self, field_name, pattern, *args, **kwargs):
        self.pattern = pattern
        super().__init__(field_name, *args, **kwargs)

    def clone_kwargs(self):
        kwargs = super().clone_kwargs()
        kwargs.update(
            pattern=self.pattern,
        )
        return kwargs
        
    class BoundPanel(FieldPanel.BoundPanel):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)           
            self.form.fields[self.field_name].__setattr__('pattern', self.panel.pattern)

        field_template_name = "edit_handlers/regex_panel_field.html"

class ServiceTypeFieldPanel(FieldPanel):
    """
    Select the service type filtered by locale of testimonial
    """

    def __init__(self, field_name, list_queryset, *args, **kwargs):
        self.list_queryset = list_queryset
        super().__init__(field_name, *args, **kwargs)

    def clone_kwargs(self):
        return {
            'heading': self.heading,
            'classname': self.classname,
            'help_text': self.help_text,
            'list_queryset': self.list_queryset,
            'field_name': self.field_name,
        }

    class BoundPanel(FieldPanel.BoundPanel):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)   
#            self.form.fields[self.field_name].widget = Select(choices=self._get_choice_list())
            self.form.fields[self.field_name].__class__.__name__ = 'typed_choice_field'

        # returns the locale_id of a testimonial given the pk id
        def parent_testimonial(self, id):
            with connection.cursor() as cursor:
                cursor.execute("select locale_id from core_testimonial where id=%s", [id])
                columns = [col[0] for col in cursor.description]
                value = [
                    dict(zip(columns, row))
                    for row in cursor.fetchall()
                ]
            return value

        # Get locale id - logic based on uri of form
        # uri ends with parent id if it is in edit mode, ends in add/?locale=code if it is in add new mode
        # Fudge to get around lack of access to parent object
        # Must be called after request is bound
        # Called from form_bound event via _get_choice_list() here
        def _get_choice_list(self):
            path = self.request.get_raw_uri()
            if path.split('/')[-2] == 'add':
                locale_id = Locale.objects.get(language_code=path.split('/')[-1].replace('?locale=','')).pk
            else:
                parent = self.parent_testimonial(id=int(path.split('/')[-2]))
                locale_id = parent[0]['locale_id']
            service_list = self.list_queryset.filter(locale_id=locale_id)
            return [('', '------')] + list(service_list.values_list('id','service'))

