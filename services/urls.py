from django.urls import path
from requests import request
from .views import *



urlpatterns = [
    
    path('api/locations/', LocationsAPIView.as_view(), name='locationsAPI'),
    path('api/locations/<int:pk>', LocationsAPIView.as_view(), name='locationsAPI'),

    path('api/workers/', WorkersAPIView.as_view(), name='workersAPI'),
    path('api/workers/<int:pk>', WorkersAPIView.as_view(), name='workersAPI'),

    path('api/schedule/', ScheduleAPIView.as_view(), name='scheduleAPI'),
    path('api/schedule/<int:pk>', ScheduleAPIView.as_view(), name='scheduleAPI'),

    path('api/specializations/', SpecializationsAPIView.as_view(), name='specializationsAPI'),
    path('api/specializations/<int:pk>', SpecializationsAPIView.as_view(), name='specializationsAPI'),

    path('', toHome, name='redirect_home'),
    path('home', HomeView.as_view(), name='home'),
    path('new_appointment', NewAppointment.as_view(), name='new_appointment'),
    path('appointment_name', AppointmentName.as_view(), name='appointment_name'),
    path('appointment_list', AppointmentList.as_view(), name='appointment_list'),
]