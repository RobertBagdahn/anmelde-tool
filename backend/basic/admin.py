from django.contrib import admin
from .models import Event, AgeGroup, EventLocation, ScoutHierarchy, \
    Registration, ZipCode, ParticipantGroup, \
    Role, MethodOfTravel, Tent, ScoutOrgaLevel, ParticipantPersonal, \
    EatHabitType, EatHabit, TravelType, \
    TentType, EventTag, EventRoleMapping, EventRole, PostalAddress, RegistrationRegisterPhase

admin.site.register(Event)
admin.site.register(AgeGroup)
admin.site.register(EventLocation)
admin.site.register(Registration)
admin.site.register(ParticipantGroup)
admin.site.register(Role)
admin.site.register(MethodOfTravel)
admin.site.register(ScoutOrgaLevel)
admin.site.register(ParticipantPersonal)
admin.site.register(EatHabitType)
admin.site.register(EatHabit)
admin.site.register(TravelType)
admin.site.register(TentType)
admin.site.register(Tent)
admin.site.register(EventRoleMapping)
admin.site.register(EventRole)
admin.site.register(PostalAddress)


@admin.register(ScoutHierarchy)
class ScoutHierarchyAdmin(admin.ModelAdmin):
    list_display = ('name', 'level', 'zip_code', 'parent', 'level')
    list_filter = ('parent', 'level')
    search_fields = ('name',)


@admin.register(ZipCode)
class ZipCodeAdmin(admin.ModelAdmin):
    list_display = ('zip_code', 'city')
    search_fields = ('zip_code', 'city')


@admin.register(RegistrationRegisterPhase)
class RegistrationRegisterPhaseAdmin(admin.ModelAdmin):
    list_display = ('name', )
    list_filter = ('name', )


@admin.register(EventTag)
class EventTagAdmin(admin.ModelAdmin):
    list_display = ('name',)
