from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, SelectDateWidget
from .models import Reservation
from django.core.exceptions import ValidationError
from django.forms.fields import EmailField
from django.forms.forms import Form


class UserForm(UserCreationForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')


class ProfileForm(ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')


class PasswordForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('password1', 'password2')


class ReservationForm(ModelForm):
    class Meta:
        model = Reservation
        fields = ('user', 'wp', 'von', 'bis')

        widgets = {
            'von': SelectDateWidget(),
            'bis': SelectDateWidget(),
        }

        labels = {
            'user': ('Benutzer'),
            'wp': ('Arbeitzplatz'),
        }
