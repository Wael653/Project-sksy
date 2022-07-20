from xmlrpc.client import boolean
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator
from django.db import models

class Unit(models.Model):
    name = models.CharField(("Name"), max_length=150, null=False)
    straße = models.CharField(("Straße"), max_length=50, default="Straße des 17. Juni", null=False)
    hausnummer = models.CharField(("Hausnummer"), max_length=10, default="135", null=False) 
    postleitzahl = models.CharField(("Postleitzahl"), max_length=5, default="10623", null=False)
    etage = models.IntegerField(("Etage"), default=0, null=False)
    def __str__(self):
        return str(self.name)


class RoomDevice(models.Model):
    bezeichnung = models.CharField(("Bezeichnung"), max_length=160)
    anzahl = models.PositiveIntegerField(("Anzahl"), null=False, default=1)
    def __str__(self):
        return str(self.bezeichnung)

class Room(models.Model):
    nummer = models.CharField(("Nummer"), max_length=15, null=False)
    geraete = models.ManyToManyField(RoomDevice)
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT)
    def __str__(self):
        return 'Raum {} in {}'.format(self.nummer, self.unit)

class WorkplaceDevice(models.Model):
    bezeichnung = models.CharField(("Bezeichnung"), max_length=160)
    anzahl = models.PositiveIntegerField(("Anzahl"), null=False, default=1)
    def __str__(self):
        return str(self.bezeichnung)

class Workplace(models.Model):
    nummer = models.PositiveIntegerField()
    geraete = models.ManyToManyField(WorkplaceDevice, blank=True)
    anzahlPersonen = models.PositiveIntegerField(default=1)
    sonstiges = models.CharField(max_length=160, null=True, blank=True)
    raum = models.ForeignKey(Room, on_delete=models.PROTECT)
    barrierefrei = models.BooleanField(("Barrierefrei"), null=True, blank=True, default=True)

    class Meta:
        ordering =['nummer']

    def __str__(self):
        return str(self.nummer)

class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    wp = models.ManyToManyField(Workplace)
    date = models.DateField()
    time = models.PositiveIntegerField(validators=[MaxValueValidator(14)])
    sonstiges = models.CharField(max_length=160, null=True)

    class Meta:
        ordering = ['date']


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    wp = models.ForeignKey(Workplace, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add= True)
    text = models.TextField(max_length = 3000, blank = True)
    rate = models.IntegerField(default = 0)
    class Meta:
        ordering = ['user']

    def __str__(self):   
      return self.user.username
    
class ProfileUser(models.Model):
    user = models.OneToOneField(User, null = True, blank = True, on_delete = models.CASCADE, related_name= "profile_user")
    first_name = models.CharField(("Vorname"), max_length=150, null= False, blank= True)
    last_name = models.CharField(("Nachname"), max_length=150, null= False, blank = True)
    username = models.CharField(("Benutzername"), max_length=100, null=True)
    email = models.EmailField(("Email-Adresse"), max_length=100, null=True)
    avatar = models.ImageField(default="anonymous.jpg", null=True, blank=True)

    def __str__(self):
	     return str(self.username)

    


     
