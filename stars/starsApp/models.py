from django.db import models
# Create your models here.


class Workplace(models.Model):
    wp_id = models.PositiveIntegerField(primary_key=True)
    number = models.IntegerField()
    reserved = models.BooleanField(default = False)
    def __str__(self):
        return self.number

class User(models.Model):
    place = models.OneToOneField( Workplace, on_delete = models.CASCADE)
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    user_id = models.PositiveIntegerField(primary_key=True)
    def __str__(self):
        return self.name

# Create your models here.
