from dataclasses import field
from django.forms import ModelForm
from django.db import models
from django import forms
from django.conf import settings
from django.core.mail import send_mail

from stars.starsApp.models import Room,Unit, Workplace, User

# from .models import Workplace, User, Unit, Room

class WorkplaceForm(ModelForm):
    class Meta:
         model = Workplace
         fields = '__all__'

class UnitForm(ModelForm):
    class Meta:
        model = Unit
        fields = '__all__'

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['room'].queryset = Room.objects.none()
        
        if 'unit' in self.data:
            try:
                unit_id = int(self.data.get('unit'))
                self.fields['room'].queryset = Room.objects.filter(unit_id=unit_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty Room queryset
        elif self.instance.pk:
            self.fields['room'].queryset = self.instance.unit.room_set.order_by('name')

class UserForm(ModelForm):
     class Meta:
         model = User
         fields = ['name','place', 'password', 'user_id']
