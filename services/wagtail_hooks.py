from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from .models import *


class WorkerAdmin(ModelAdmin):
    model = Worker
    menu_label = 'Workers'
    add_to_settings_menu = False
    exclude_from_explorer = False
    menu_order = 100
    search_fields = ('name',)

class ScheduleAdmin(ModelAdmin):
    model = Schedule
    menu_label = 'Schedule'
    add_to_settings_menu = False
    exclude_from_explorer = False
    menu_order = 100
    search_fields = ('date',)

class SpecializationAdmin(ModelAdmin):
    model = Specialization
    menu_label = 'Specializations'
    add_to_settings_menu = False
    exclude_from_explorer = False
    menu_order = 100

class AppointmentAdmin(ModelAdmin):
    model = Appointment
    menu_label = 'Appointments'
    add_to_settings_menu = False
    exclude_from_explorer = False
    menu_order = 100
    search_fields = ('client', 'date')

class LocationAdmin(ModelAdmin):
    model = Location
    menu_label = 'Locations'
    add_to_settings_menu = False
    exclude_from_explorer = False
    menu_order = 100




modeladmin_register(ScheduleAdmin)
modeladmin_register(AppointmentAdmin)
modeladmin_register(WorkerAdmin)
modeladmin_register(SpecializationAdmin)
modeladmin_register(LocationAdmin)