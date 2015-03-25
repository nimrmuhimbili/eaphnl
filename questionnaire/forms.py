import django
from django import forms
from django.template import Template
from django.forms.models import modelform_factory, inlineformset_factory
from django.contrib.auth.models import User, Group

from djangoformsetjs.utils import formset_media_js

try:
    from django.utils.timezone import now
except ImportError:
    from datetime import datetime
    now = datetime.now

from questionnaire.models import Form, Field, FormEntry, FieldEntry
from questionnaire import fields, widgets
from questionnaire.utils import split_choices


class DesignedForm(forms.ModelForm):

    class Meta:
        model = Form
        fields = '__all__'
        widgets = {
            'version_date': widgets.DateAddonWidget()
        }


class FieldForm(forms.ModelForm):

    class Meta:
        model = Field
        exclude = ('number',)
        widgets = {
            'form': forms.HiddenInput
        }

    class Media(object):
        js = formset_media_js


FieldsFormset = inlineformset_factory(Form, Field, form=FieldForm, extra=0, can_delete=True)


class FormEntryForm(forms.ModelForm):
    field_entry_model = FieldEntry

    class Meta:
        model = FormEntry
        exclude = ('form', 'entry_time')

    def __init__(self, form, *args, **kwargs):
        self.form = form
        self.form_fields = form.fields.all()
        initial = kwargs.pop('initial', {})
        # If a FormEntry instance is given to edit, store it's field
        # values for using as initial data.
        field_entries = {}
        if kwargs.get('instance'):
            self.entry_fields = kwargs['instance'].fields.values_list('field_id', flat=True)
            for field_entry in kwargs['instance'].fields.all():
                field_entries[field_entry.field_id] = field_entry.response
        super(FormEntryForm, self).__init__(*args, **kwargs)
        for field in self.form_fields:
            field_key = field.name
            field_class = fields.CLASSES[field.response_type]
            field_widget = fields.WIDGETS.get(field.response_type)
            field_args = {
                'label': field.label,
                'required': field.required,
                'help_text': field.help_text,
            }
            arg_names = field_class.__init__.__code__.co_varnames
            if 'max_length' in arg_names:
                field_args['max_length'] = fields.FIELD_MAX_LENGTH
            if 'choices' in arg_names:
                choices = list(field.get_choices())
                choices.insert(0, ("",""))
                field_args['choices'] = choices
            if field_widget is not None:
                field_args['widget'] = field_widget
            # If a form model instance is given (eg we're editing a
            # form response), then use the instance's value for the
            # field.
            initial_val = None
            try:
                initial_val = field_entries[field.id]
            except KeyError:
                try:
                    initial_val = field_entries[field_key]
                except KeyError:
                    pass
            if initial_val:
                if field.response_type in fields.MULTIPLE:
                    initial_val = split_choices(initial_val)
                if field.response_type == fields.CHECKBOX:
                    initial_val = initial_val != "False"
                self.initial[field_key] = initial_val
            self.fields[field_key] = field_class(**field_args)

            # Add identifying css classes
            css_class = ""
            if field.response_type not in [fields.CHECKBOX, fields.CHECKBOX_MULTIPLE, fields.RADIO]:
                css_class += "form-control input-sm"
            self.fields[field_key].widget.attrs['class'] = css_class

    def rows(self, section_fields, step=1):
        row = []
        rows = [row]
        expect = None
        for form_field, field in section_fields:
            if form_field.column == expect or expect is None:
                row.append(field)
            else:
                row = [field]
                rows.append(row)
            expect = form_field.column + step
        return rows

    def sections(self, key=lambda field: field[0].section):
        from itertools import groupby
        import collections
        section_dict = collections.OrderedDict()
        sections = groupby(zip(self.form_fields, self), key)
        for section, section_fields in sections:
            section_dict[section] = self.rows(section_fields)
        return section_dict

    def clean(self):
        cleaned_data = self.cleaned_data
        for field in self.form_fields:
            if field.unique:
                field_key = field.name
                response = cleaned_data.get(field_key)
                qs = self.field_entry_model.objects.filter(response=response)
                if field.id in self.entry_fields:
                    qs = qs.exclude(field_id=field.id)
                if qs.count() > 0:
                    err_msg = "This field must be unique."
                    self._errors[field_key] = self.error_class([err_msg])
        return cleaned_data

    def save(self, **kwargs):
        entry = super(FormEntryForm, self).save(commit=False)
        entry.form = self.form
        entry.entry_time = now()
        entry.save()
        entry_fields = entry.fields.values_list('field_id', flat=True)
        new_entry_fields = []
        for field in self.form_fields:
            field_key = field.name
            response = self.cleaned_data[field_key]
            if isinstance(response, list):
                response = ','.join([v.strip() for v in response])
            if field.id in entry_fields:
                field_entry = entry.fields.get(field_id=field.id)
                field_entry.response = response
                field_entry.save()
            else:
                new = {'entry': entry, 'field_id': field.id, 'response': response}
                new_entry_fields.append(self.field_entry_model(**new))
        if new_entry_fields:
            if django.VERSION >= (1, 4, 0):
                self.field_entry_model.objects.bulk_create(new_entry_fields)
            else:
                for field_entry in new_entry_fields:
                    field_entry.save()
        return entry


class EntriesForm(forms.Form):

    def __init__(self, form, request, formentry=FormEntry, fieldentry=FieldEntry, *args, **kwargs):
        self.form = form
        self.request = request
        self.formentry = formentry
        self.fieldentry = fieldentry
        self.form_fields = form.fields.all()
        super(EntriesForm, self).__init__(*args, **kwargs)
        for field in self.form_fields:
            field_key = "field_%s" %field.id
            # Checkbox for including in export
            self.fields["%s_export" %field_key] = forms.BooleanField(
                label=field.name, initial=True, required=False)

    def posted_data(self, field):
        """
        Wrapper for self.cleaned_data that returns True on
        field_id_export fields when the form hasn't been posted to,
        to facilitate show/export URLs that export all entries without
        a form submission.
        """
        try:
            return self.cleaned_data[field]
        except (AttributeError, KeyError):
            return field.endswith('_export')

    def columns(self):
        """
        Returns the list of selected column names.
        """
        fields = [f.name for f in self.form_fields
                  if self.posted_data("field_%s_export" %f.id)
        ]
        return fields

    def rows(self, csv=False):
        """
        Returns each row based on the selected criteria.
        """
        field_indexes = {}
        date_field_ids = []
        for field in self.form_fields:
            if self.posted_data("field_%s_export" % field.id):
                field_indexes[field.id] = len(field_indexes)
                if field.response_type == fields.DATE:
                    date_field_ids.append(field.id)
        num_columns = len(field_indexes)

        # Get field entries for the given form
        field_entries = self.fieldentry.objects.filter(entry__form=self.form
                        ).order_by("-entry__id").select_related("entry")

        # Loop through each field value ordered by entry, building up each
        # entry as a row.
        current_entry = None
        current_row = None
        valid_row = True
        for field_entry in field_entries:
            if field_entry.entry_id != current_entry:
                # New entry, write out the current row and start a new one.
                if valid_row and current_row is not None:
                    if not csv:
                        current_row.insert(0, current_entry)
                    yield current_row
                current_entry = field_entry.entry_id
                current_row = [""]*num_columns
                valid_row = True
            field_response = field_entry.response or ""
            # Only use values for fields that were selected.
            try:
                current_row[field_indexes[field_entry.field_id]] = field_response
            except KeyError:
                pass
        if valid_row and current_row is not None:
            if not csv:
                current_row.insert(0, current_entry)
            yield current_row


class UserProfileForm(forms.ModelForm):
    group = forms.ModelChoiceField(queryset=Group.objects.all(), required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'group']

    def save(self, commit=True):
        user = super(UserProfileForm, self).save(commit=False)
        user.set_password('123456')
        if commit:
            user.save()
            user.groups.add(self.cleaned_data.get('group'))
        return user