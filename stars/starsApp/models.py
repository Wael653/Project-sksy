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


class Room(models.Model):
    nummer = models.CharField(max_length=1, choices= [('A','A'),('B','B'),('C','C')], unique= True)
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT, blank = True)
    def __str__(self):
        return str(self.nummer)

class WorkplaceDevice(models.Model):
    bezeichnung = models.CharField(("Bezeichnung"), max_length=160)
    def __str__(self):
        return str(self.bezeichnung)

class Workplace(models.Model):
    nummer = models.PositiveIntegerField()
    geraete = models.ManyToManyField(WorkplaceDevice)
    anzahlPersonen = models.PositiveIntegerField(default=1)
    raum = models.ForeignKey(Room, on_delete=models.PROTECT)
    sonstiges = models.CharField(max_length=160)

    class Meta:
        ordering =['nummer']

    def __str__(self):
        return str(f'{self.raum}{self.nummer}')


class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    wp = models.ManyToManyField(Workplace)
    date = models.DateField()
    time = models.PositiveIntegerField(validators=[MaxValueValidator(14)])
    sonstiges = models.CharField(max_length=160, null=True)

    class Meta:
        ordering = ['user']

    # wird noch angepasst
    def __str__(self):
        return str(f'{self.user} --> {self.wp.first()}')

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    wp = models.ForeignKey(Workplace, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add= True)
    text = models.TextField(max_length = 3000, blank = True)
    rate = models.IntegerField(default = 0)
    def __str__(self):   
      return self.user.username

