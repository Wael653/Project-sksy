from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator
from django.db import models

class Workplace(models.Model):
    nummer = models.PositiveIntegerField()
    geraete = models.CharField(max_length=160, null=True)
    anzahlPersonen = models.PositiveIntegerField(default=1)
    sonstiges = models.CharField(max_length=160)

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
        ordering = ['user']
