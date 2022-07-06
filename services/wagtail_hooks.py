from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from .models import *

class LocationAdmin(ModelAdmin):
    model = Location
    menu_label = 'Locations'
    add_to_settings_menu = False
    exclude_from_explorer = False
    menu_order = 100

class WorkerAdmin(ModelAdmin):
    model = Worker
    menu_label = 'Workers'
    add_to_settings_menu = False
    exclude_from_explorer = False
    menu_order = 100

class ScheduleAdmin(ModelAdmin):
    model = Schedule
    menu_label = 'Schedule'
    add_to_settings_menu = False
    exclude_from_explorer = False
    menu_order = 100

class SpecializationAdmin(ModelAdmin):
    model = Specialization
    menu_label = 'Specializations'
    add_to_settings_menu = False
    exclude_from_explorer = False
    menu_order = 100




modeladmin_register(ScheduleAdmin)
modeladmin_register(WorkerAdmin)
modeladmin_register(LocationAdmin)
modeladmin_register(SpecializationAdmin)