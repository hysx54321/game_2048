import random

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class SaveGameForm(forms.Form):
    score = forms.IntegerField()
    second = forms.IntegerField()
    move = forms.IntegerField()
    reconstruction = forms.IntegerField()

    def clean_score(self):
        data = self.cleaned_data['score']

        # Check if the number is too large.
        if data > 10000 or data < 0:
            raise ValidationError(_('Invalid number - it must be between 0 and 10000'))

        # Remember to always return the cleaned data.
        return data + random.randint(1, 50)


class NewUserForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()

    def clean_username(self):
        data = self.cleaned_data['username']
        return data
