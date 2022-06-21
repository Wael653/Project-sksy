from django.forms import ModelForm
from .models import User
from django import forms
from django.conf import settings
from django.core.mail import send_mail

class UserForm(ModelForm):
     class Meta:
         model = User
         fields = ['name','place', 'password', 'user_id']