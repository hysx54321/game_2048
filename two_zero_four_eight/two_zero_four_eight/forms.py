import random

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class SaveGameForm(forms.Form):
    magic_number = forms.IntegerField(help_text="Enter a magic number between 0 and 10000 (default 888).")

    def clean_magic_number(self):
        data = self.cleaned_data['magic_number']

        # Check if the number is too large.
        if data > 10000 or data < 0:
            raise ValidationError(_('Invalid number - it must be between 0 and 10000'))

        # Remember to always return the cleaned data.
        return data + random.randint(1, 50)
