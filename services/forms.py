from cProfile import label
from django import forms
from requests import request
from .models import *

class NewAppointmentForm(forms.Form):
    client = forms.CharField(max_length=255, label='Your name:')
    worker = forms.ModelChoiceField(queryset=Worker.objects.all().order_by('name'), label='Select worker:')
    location = forms.ModelChoiceField(queryset=Location.objects.all().order_by('name'), label='Select location:')
    date = forms.DateField(label='Date:', widget=forms.TextInput(attrs={'type': 'date'}))
    start = forms.TimeField(label='Time',widget=forms.TextInput(attrs={'type': 'time'}))
    end = forms.TimeField(label='Time',widget=forms.TextInput(attrs={'type': 'time'}))

class NameForm(forms.Form):
    name = forms.CharField(max_length=255)
    next = forms.BooleanField(label='Only future appointments', required=False)