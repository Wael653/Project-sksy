from django.forms import ModelForm
from django.db import models

from .models import User, Workplace


class UserForm(ModelForm):
     class Meta:
         model = User
         fields = ['name','place', 'password', 'user_id']



