from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import make_password

class LoginOrRegisterForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())