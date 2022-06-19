from django.core.validators import MaxValueValidator
from django.db import models

# Create your models here.


class Workplace(models.Model):
    nummer = models.PositiveIntegerField()
    geraete = models.CharField(max_length=160)
    anzahlPersonen = models.PositiveIntegerField(default=1)
    sonstiges = models.CharField(max_length=160)
