from django.forms import ModelForm
from django.db import models
from django import forms
from django.conf import settings
from django.core.mail import send_mail

from .models import User, Workplace

class WorkplaceForm(ModelForm):
    class Meta:
         model = Workplace
         fields = ['wp_id', 'number','reserved']

class UserForm(ModelForm):
     class Meta:
         model = User
         fields = ['name','place', 'password', 'user_id']
