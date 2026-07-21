from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import *

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ('name', 'description', 'industry', 'city', 'website', 'logo', 'employee_count')

        