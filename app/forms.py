from django import forms
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(max_length=255, required=True)
    password = forms.CharField(max_length=255, required=True)


class SignupForm(forms.Form):
    username = forms.CharField(max_length=255, required=True)
    email = forms.EmailField(max_length=255, required=True)
    password = forms.CharField(max_length=255, min_length=8, required=True)
    confirm_password = forms.CharField(max_length=255, min_length=8, required=True)

    def clean_email(self):
        clean_email = self.cleaned_data.get('email')
        if User.objects.filter(email=clean_email).exists():
            raise forms.ValidationError('Email is already used')
        return clean_email

    def clean_username(self):
        clean_username = self.cleaned_data.get('username')
        if User.objects.filter(username=clean_username).exists():
            raise forms.ValidationError('Username is already used')
        return clean_username

    def clean(self):
        clean_data = super().clean()
        if clean_data.get('password') != clean_data.get('confirm_password'):
            self.add_error('confirm_password', 'Password does not match')
        return clean_data
