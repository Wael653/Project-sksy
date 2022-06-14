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
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=160)
    creation_date = models.DateTimeField()
    state = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(1)])