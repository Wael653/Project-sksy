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
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')



class ContactForm(forms.Form):

    name = forms.CharField(max_length=120)
    email = forms.EmailField(label='E-Mail-Adresse')
    betreff = forms.CharField(max_length=120)
    nachricht = forms.CharField(widget=forms.Textarea)

    def get_info(self):
        """
        Method that returns formatted information
        :return: subject, msg
        """
        # Cleaned data
        cl_data = super().clean()

        name = cl_data.get('name').strip()
        from_email = cl_data.get('email')
        betreff = cl_data.get('betreff')

        msg = f'{name} mit der E-Mail-Adresse {from_email} schrieb: '
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





