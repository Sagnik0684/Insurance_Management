from django import forms
from django.contrib.auth.models import User
from . import models

from django.core.exceptions import ValidationError
import re
from .models import Customer  # Assuming Customer is the model for customer form


class CustomerUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), min_length=8)
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password']

    def clean_password(self):
        password = self.cleaned_data.get('password')

        # Check if password contains at least one special character
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValidationError('Password must contain at least one special character.')
        
        # Check if password contains both letters and numbers
        if not re.search(r'[A-Za-z]', password) or not re.search(r'[0-9]', password):
            raise ValidationError('Password must contain both letters and numbers.')

        # Check if password length is at least 8 characters (already done with min_length)
        if len(password) < 8:
            raise ValidationError('Password must be at least 8 characters long.')

        return password

    def clean_username(self):
        username = self.cleaned_data.get('username')

        # Check if username is unique
        if User.objects.filter(username=username).exists():
            raise ValidationError('This username is already taken.')

        return username


class CustomerForm(forms.ModelForm):
    mobile = forms.CharField(max_length=10)

    class Meta:
        model = Customer
        fields = ['address', 'mobile', 'profile_pic']

    def clean_mobile(self):
        mobile = self.cleaned_data.get('mobile')

        # Check if mobile number has exactly 10 digits
        if not re.match(r'^\d{10}$', mobile):
            raise ValidationError('Mobile number must be exactly 10 digits long.')

        return mobile

from .models import CustomerPolicy

from django import forms
from .models import CustomerPolicy

class CustomerPolicyForm(forms.ModelForm):
    class Meta:
        model = CustomerPolicy
        fields = ['policy_number', 'policy_name', 'provider_name', 'start_date', 'renewal_date']
        widgets = {
            'start_date': forms.TextInput(attrs={'placeholder': 'mm/dd/yyyy', 'type': 'date'}),
            'renewal_date': forms.TextInput(attrs={'placeholder': 'mm/dd/yyyy', 'type': 'date'}),
        }


class ChatbotForm(forms.Form):
    message = forms.CharField(max_length=200,widget=forms.TextInput(attrs={'placeholder': 'Type your message...'}))