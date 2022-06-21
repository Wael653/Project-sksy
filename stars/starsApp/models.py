from django.core.validators import MaxValueValidator
from django.db import models

# Create your models here.
class Contact(models.Model):
    name= models.CharField(max_length=50)
    email = models.EmailField()
    subject = models.CharField(max_length = 50)
    message = models.TextField()
    def __str__(self):
        return self.name

class Workplace(models.Model):
    nummer = models.PositiveIntegerField()
    geraete = models.CharField(max_length=160, null=True)
    anzahlPersonen = models.PositiveIntegerField(default=1)
    sonstiges = models.CharField(max_length=160, null=True)
