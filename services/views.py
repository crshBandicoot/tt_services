from datetime import date, datetime, time
from http import client
from operator import ne
from re import L, template
from pytz import timezone
from requests import delete
from rest_framework.response import Response as restResponse
from rest_framework import viewsets, generics, views
from .serializers import *
from .models import *
from django.views.generic import TemplateView, ListView, FormView
from .forms import NewAppointmentForm, NameForm
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader


class HomeView(TemplateView):
    template_name = 'home.html'

def toHome(request):
    return HttpResponseRedirect(reverse('home'))

class AppointmentName(FormView):
    template_name = 'appointment_name.html'
    form_class = NameForm

class AppointmentList(ListView):
    def get(self, request):
        template_name = 'appointment_list.html'
        template = loader.get_template(template_name)
        name = request.GET.get('name')
        next = request.GET.get('next', None)
        queryset = Appointment.objects.filter(client=name)
        if next:
            queryset = queryset.filter(start__gte=datetime.now())
        context = {'object_list': queryset}
        return HttpResponse(template.render(context, request))

class NewAppointment(FormView):
    form_class = NewAppointmentForm
    template_name = 'appointment_form.html'
    success_url = reverse_lazy('home')
    def form_valid(self, form):
        client = form.data['client']
        date = form.data['date']
        start_appointment = form.data['start']
        start_appointment = datetime.strptime(start_appointment, '%H:%M').time()
        procedure = form.data['procedure']
        procedure = Specialization.objects.get(id=procedure)
        worker = Worker.objects.get(specialization=procedure)

        start_date = datetime(1,1,1, start_appointment.hour, start_appointment.minute)
        end_appointment = (start_date + timedelta(hours=1)).time()
        schedule = Schedule.objects.order_by('start').filter(worker=worker).filter(date=date)
        
        for appointment in schedule:
            start, end = appointment.start, appointment.end
            if start_appointment >= start and start_appointment <= end_appointment:
                return HttpResponse('Busy time! Appointment not created!<br><a href="home">Go back to mainpage</a>')
            if end_appointment >= end and end_appointment <= end:
                return HttpResponse('Busy time! Appointment not created!<br><a href="home">Go back to mainpage</a>')
        Schedule.objects.create(worker=worker, date=date, start=start_appointment, end=end_appointment)
        
        Appointment.objects.create(client=client, date=date, start=start_appointment, procedure=procedure)
        return HttpResponse('Succesful!<br><a href="home">Go back to mainpage</a>')

class SpecializationsAPIView(views.APIView):

    def get(self, request, **kwargs):
        pk = kwargs.get('pk', None)
        if pk:
            queryset = Specialization.objects.filter(id=pk)
            return restResponse(SpecializationSerializer(queryset, many=True).data)
        queryset = Specialization.objects.all()
        return restResponse(SpecializationSerializer(queryset, many=True).data)

    def post(self, request):
        serializer = SpecializationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return restResponse({'POST': serializer.data})
    
    def put(self, request, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            return restResponse({'Error: ': 'PUT not allowed without PK!'})
        try:
            instance = Specialization.objects.get(id=pk)
        except:
            return restResponse({'Error: ': 'Entry not found!'})
        
        serializer = SpecializationSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return restResponse({'PUT': serializer.data})

    def delete(self, request, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            return restResponse({'Error: ': 'DELETE not allowed without PK!'})
        try:
            instance = Specialization.objects.get(id=pk)
        except:
            return restResponse({'Error: ': 'Entry not found!'})
        instance.delete()
        return restResponse({'DELETE: ': pk})
        
class LocationsAPIView(views.APIView):

    def get(self, request, **kwargs):
        pk = kwargs.get('pk', None)
        if pk:
            queryset = Location.objects.filter(id=pk)
            return restResponse(LocationSerializer(queryset, many=True).data)
        queryset = Location.objects.all()
        return restResponse(LocationSerializer(queryset, many=True).data)

    def post(self, request):
        serializer = LocationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return restResponse({'POST': serializer.data})
    
    def put(self, request, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            return restResponse({'Error: ': 'PUT not allowed without PK!'})
        try:
            instance = Location.objects.get(id=pk)
        except:
            return restResponse({'Error: ': 'Entry not found!'})
        
        serializer = LocationSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return restResponse({'PUT': serializer.data})

    def delete(self, request, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            return restResponse({'Error: ': 'DELETE not allowed without PK!'})
        try:
            instance = Location.objects.get(id=pk)
        except:
            return restResponse({'Error: ': 'Entry not found!'})
        instance.delete()
        return restResponse({'DELETE: ': pk})

class WorkersAPIView(views.APIView):

    def get(self, request, **kwargs):
        pk = kwargs.get('pk', None)
        if pk:
            queryset = Worker.objects.filter(id=pk)
            free_time = request.GET.get('free_time', None)
            date = request.GET.get('date', None)
            if free_time and date:
                date = datetime.strptime(date, '%m-%d-%Y').date()
                worker = Worker.objects.get(id=pk)
                job_start = worker.job_start
                job_end = worker.job_end
                appointments = Schedule.objects.order_by('start').filter(worker=pk).filter(date=date)
                free = []
                busy = []
                for appointment in appointments:
                    start, end = appointment.start, appointment.end
                    busy.append((start, end))
                if not busy:
                    free.append((job_start, job_end))
                elif len(busy) == 1:
                    free.append((job_start, busy[0][0]))
                    free.append((busy[0][1], job_end))
                else:
                    free.insert(0, (job_start, busy[0][0]))
                    for i in range(len(busy)-1):
                        previous = busy[i]
                        next = busy[i+1]
                        if previous[1] != next[0]:
                            free.append((previous[1], next[0]))
                    free.append((busy[-1][1], job_end))
                return restResponse(WorkerSerializer(queryset, many=True).data + [{'free_time': free}])
            return restResponse(WorkerSerializer(queryset, many=True).data)
            
            
            
        specialization =  request.GET.get('specialization', None)
        if specialization:
            queryset = Worker.objects.filter(specialization=specialization)
        else:
            queryset = Worker.objects.all()
        return restResponse(WorkerSerializer(queryset, many=True).data)

    def post(self, request):
        serializer = WorkerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return restResponse({'POST': serializer.data})
    
    def put(self, request, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            return restResponse({'Error: ': 'PUT not allowed without PK!'})
        try:
            instance = Worker.objects.get(id=pk)
        except:
            return restResponse({'Error: ': 'Entry not found!'})
        
        serializer = WorkerSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return restResponse({'PUT': serializer.data})
    
    def delete(self, request, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            return restResponse({'Error: ': 'DELETE not allowed without PK!'})
        try:
            instance = Worker.objects.get(id=pk)
        except:
            return restResponse({'Error: ': 'Entry not found!'})
        instance.delete()
        return restResponse({'DELETE: ': pk})

class ScheduleAPIView(views.APIView):

    def get(self, request, **kwargs):
        pk = kwargs.get('pk', None)
        date =  request.GET.get('date', None)
        worker =  request.GET.get('worker', None)
        queryset = Schedule.objects.all().order_by('date', 'start')
        if pk:
            queryset = queryset.get(id=pk)
            return restResponse(ScheduleSerializer(queryset).data)
        
        if date:
            date = datetime.strptime(date, '%Y-%m-%d').date()
            queryset = queryset.filter(date=date)
            
        if worker:
            queryset = queryset.filter(worker=worker)
        return restResponse(ScheduleSerializer(queryset, many=True).data)
        
    def post(self, request):
        serializer = ScheduleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return restResponse({'POST': serializer.data})
    
    def put(self, request, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            return restResponse({'Error: ': 'PUT not allowed without PK!'})
        try:
            instance = Schedule.objects.get(id=pk)
        except:
            return restResponse({'Error: ': 'Entry not found!'})
        
        serializer = ScheduleSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return restResponse({'PUT': serializer.data})

    def delete(self, request, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            return restResponse({'Error: ': 'DELETE not allowed without PK!'})
        try:
            instance = Schedule.objects.get(id=pk)
        except:
            return restResponse({'Error: ': 'Entry not found!'})
        instance.delete()
        return restResponse({'DELETE: ': pk})


class AppointmentsAPIView(views.APIView):

    def get(self, request, **kwargs):
        pk = kwargs.get('pk', None)
        date =  request.GET.get('date', None)
        procedure =  request.GET.get('procedure', None)
        queryset = Appointment.objects.all().order_by('date', 'start')
        if pk:
            queryset = queryset.get(id=pk)
            return restResponse(AppointmentSerializer(queryset).data)
        
        if date:
            date = datetime.strptime(date, '%Y-%m-%d').date()
            queryset = queryset.filter(date=date)
            
        if procedure:
            queryset = queryset.filter(procedure=procedure)
        return restResponse(AppointmentSerializer(queryset, many=True).data)
        
    def post(self, request):
        serializer = AppointmentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return restResponse({'POST': serializer.data})

    def delete(self, request, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            return restResponse({'Error: ': 'DELETE not allowed without PK!'})
        try:
            instance = Appointment.objects.get(id=pk)
        except:
            return restResponse({'Error: ': 'Entry not found!'})
        instance.delete()
        return restResponse({'DELETE: ': pk})
