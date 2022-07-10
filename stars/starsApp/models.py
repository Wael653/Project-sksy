from xmlrpc.client import boolean
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator
from django.db import models
##from star_ratings import AbstractBaseRating

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
    def __str__(self):
        return str(self.nummer)

class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    wp = models.ForeignKey(Workplace, on_delete=models.PROTECT)
    von = models.DateTimeField()
    bis = models.DateTimeField()
    sonstiges = models.CharField(max_length=160, null=True, blank=True)
    def __str__(self):
        return str(self.user + self.wp + " from " + self.von + " bis " + self.bis)