from django.db import connection
from django.forms.widgets import Select
from wagtail_localize.synctree import Locale
from wagtail.admin.edit_handlers import FieldPanel

class ServiceTypeFieldPanel(FieldPanel):
    """
    Select the service type filtered by locale of testimonial
    If new, presumes default locale
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

    # returns the locale_id of a testimonial given the pk id
    def parent_testimonial(self, id):
        with connection.cursor() as cursor:
            cursor.execute("select locale_id from core_testimonial where id=%s", [id])
            columns = [col[0] for col in cursor.description]
            value = [
                dict(zip(columns, row))
                for row in cursor.fetchall()
            ]
            print(value)
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

    # declare widget with choices (this event seems to get called twice)
    # change field type to typed_choice_field otherwise it'll appear as a text field with
    # dropdown behaviour
    def on_form_bound(self):
        self.form.fields[self.field_name].widget = Select(choices=self._get_choice_list())
        self.form.fields[self.field_name].__class__.__name__ = 'typed_choice_field'
        super().on_form_bound()
