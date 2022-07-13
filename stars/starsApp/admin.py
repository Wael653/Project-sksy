from django.contrib import admin
from .models import Unit, Room, Workplace, WorkplaceDevice, Review

# Register your models here.
admin.site.register(Workplace)
admin.site.register(Unit)
admin.site.register(Room)
admin.site.register(WorkplaceDevice)
admin.site.register(Review)
