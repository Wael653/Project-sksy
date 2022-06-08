from django.core.validators import MaxValueValidator
from django.db import models


# Create your models here.

class Workplace(models.Model):
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=160)
    creation_date = models.DateTimeField()
    state = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(1)]) #Arbeitsplatz ist bei 0 leer und bei 1 besetzt
