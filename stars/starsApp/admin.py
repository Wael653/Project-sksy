from django.contrib import admin
from .models import Workplace, Reservation, Review, Unit, WorkplaceDevice, Room


# Register your models here.
admin.site.register(Unit)
admin.site.register(WorkplaceDevice)
admin.site.register(Workplace)
admin.site.register(Reservation)
admin.site.register(Review)
admin.site.register(Room)