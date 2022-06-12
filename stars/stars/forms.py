from django.forms import ModelForm
from django.db import models

from .models import User, Workplace


class WorkplaceForm(ModelForm):
    class Meta:
         model = Workplace
         fields = ['wp_id', 'number','reserved']


class UserForm(ModelForm):
     class Meta:
         model = User
         fields = ['name','place', 'password', 'user_id']



