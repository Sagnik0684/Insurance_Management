from django import forms
from django.contrib.auth.models import User
from . import models


class CustomerUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }

class CustomerForm(forms.ModelForm):
    class Meta:
        model=models.Customer
        fields=['address','mobile','profile_pic']

from .models import CustomerPolicy

class CustomerPolicyForm(forms.ModelForm):
    class Meta:
        model = CustomerPolicy
        fields = ['policy_number', 'policy_name', 'provider_name', 'start_date', 'renewal_date']