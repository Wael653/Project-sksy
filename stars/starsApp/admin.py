from django.contrib import admin
from .models import Unit, Room, Workplace, WorkplaceDevice, Review
from .models import Unit, Room, RoomDevice, Workplace, WorkplaceDevice

# Register your models here.
admin.site.register(Workplace)
admin.site.register(Unit)
admin.site.register(Room)
admin.site.register(Review)
admin.site.register(RoomDevice)
admin.site.register(WorkplaceDevice)

