from django.contrib import admin
from .models import Event, AgeGroup, EventLocation, EventContact


admin.site.register(Event)
admin.site.register(AgeGroup)
admin.site.register(EventLocation)
admin.site.register(EventContact)
