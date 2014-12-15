from django import forms

from questionnaire import widgets


FIELD_MAX_LENGTH = 2000

NUMBER = 1
DECIMAL = 2
TEXT = 3
TEXTAREA = 4
RADIO = 5
CHECKBOX = 6
CHECKBOX_MULTIPLE = 7
SELECT = 8
SELECT_MULTIPLE = 9
DATE = 10
TIME = 11
DATE_TIME = 12

NAMES = (
    (NUMBER, 'Integer'),
    (DECIMAL, 'Decimal'),
    (TEXT, 'Single line text'),
    (TEXTAREA, 'Multiple line text'),
    (RADIO, 'Radio'),
    (CHECKBOX, 'Checkbox'),
    (CHECKBOX_MULTIPLE, 'Multiple checkbox'),
    (SELECT, 'Single select'),
    (SELECT_MULTIPLE, 'Multiple select'),
    (DATE, 'Date'),
    (TIME, 'Time'),
    (DATE_TIME, 'Date/time'),
)

CLASSES = {
    NUMBER: forms.IntegerField,
    DECIMAL: forms.DecimalField,
    TEXT: forms.CharField,
    TEXTAREA: forms.CharField,
    RADIO: forms.ChoiceField,
    CHECKBOX: forms.BooleanField,
    CHECKBOX_MULTIPLE: forms.MultipleChoiceField,
    SELECT: forms.ChoiceField,
    SELECT_MULTIPLE: forms.MultipleChoiceField,
    DATE: forms.DateField,
    TIME: forms.TimeField,
    DATE_TIME: forms.DateTimeField,
}

WIDGETS = {
    TEXTAREA: forms.Textarea,
    RADIO: forms.RadioSelect,
    CHECKBOX_MULTIPLE: forms.CheckboxSelectMultiple,
    DATE: widgets.DateAddonWidget,
}

# Some helper groupings of field types.
CHOICES = (CHECKBOX, SELECT, RADIO)
MULTIPLE = (CHECKBOX_MULTIPLE, SELECT_MULTIPLE)