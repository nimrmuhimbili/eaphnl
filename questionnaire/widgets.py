from django import forms
from django.forms.utils import flatatt
from django.utils.html import force_text, format_html

from eaphnl import settings


class DateAddonWidget(forms.DateInput):

    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        if value != '':
            # Only add the 'value' attribute if a value is non-empty.
            final_attrs['value'] = force_text(self._format_value(value))
        output = """
            <div class="input-group date">
                <input{0} />
                <span class="input-group-addon">
                    <i class="fa fa-calendar"></i>
                </span>
            </div>
        """
        return format_html(output, flatatt(final_attrs))