from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, SelectDateWidget
from .models import Reservation
from django.core.exceptions import ValidationError
from django.forms.fields import EmailField
from django.forms.forms import Form
from django.core.mail import send_mail
from django.conf import settings

class UserForm(UserCreationForm):
    password1 = forms.CharField(
        label="Passwort",
        strip=False,
        widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label="Passwort",
        strip=False,
        widget=forms.PasswordInput
    )
    first_name = forms.CharField(max_length = 50, label = "Vorname")
    last_name = forms.CharField(max_length= 50, label = "Nachname")
    username = forms.CharField(max_length= 100, label = "Benutzername")
    email = forms.EmailField(max_length = 50, label = "E-Mail-Adresse")

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['first_name'].widget.attrs.update({'class': 'form-control', 'style': "width: 700px", 'required': 'True'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control', 'style': "width: 700px", 'required': 'True'})
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'aria-describedby':'emailHelp'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': "name@example.com", 'required': 'True'}) 
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'aria-describedby':'emailHelp'})

class LoginForm(forms.Form):
      username = forms.CharField(label = "Benutzername", widget=forms.TextInput(attrs = {'class': 'form-control', 'style': "width: 700px"}))
      password = forms.CharField(label = "Passwort", widget=forms.PasswordInput(attrs = {'class': 'form-control', 'style': "width: 700px"}))



class ContactForm(forms.Form):

    vorname = forms.CharField(max_length=120, widget = forms.TextInput(attrs = {"class": "form-control", "style": "margin: 0 0 0 0"}), required = True )
    nachname = forms.CharField(max_length=120, widget = forms.TextInput(attrs = {"class": "form-control", "style": "margin: 0 0 0 0"}), required = True )
    email = forms.EmailField(label='E-Mail-Adresse', max_length = 80, widget = forms.EmailInput(attrs = {"class": "form-control"}), required = True)
    betreff = forms.CharField(max_length=120, widget = forms.TextInput(attrs = {"class": "form-control"}) )
    nachricht = forms.CharField(widget = forms.Textarea(attrs = {"class": "form-control", "rows": 5 }), required= True)

    def get_info(self):
        """
        Method that returns formatted information
        :return: subject, msg
        """
        # Cleaned data
        cl_data = super().clean()

        vorname = cl_data.get('vorname').strip()
        nachname = cl_data.get('nachname').strip()
        from_email = cl_data.get('email')
        betreff = cl_data.get('betreff')
        msg = f'{vorname} {nachname} mit der E-Mail-Adresse: {from_email} schrieb: '
        msg += cl_data.get('nachricht')

        return betreff, msg

    def send(self):

        betreff, msg = self.get_info()

        send_mail(
            subject=betreff,
            message=msg,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.RECIPIENT_ADDRESS]
        )

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