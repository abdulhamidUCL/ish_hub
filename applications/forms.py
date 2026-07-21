from django import forms
from .models import *

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ('cover_letter', 'cover_letter_file',)

