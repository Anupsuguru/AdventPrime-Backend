# forms.py
from django import forms
from django.core.exceptions import ValidationError
import re


class SearchForm(forms.Form):
    query = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'search-form search-input',
                'placeholder': 'Search By Title of Workshop...',
            }
        )
    )
