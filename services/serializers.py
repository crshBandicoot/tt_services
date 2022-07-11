from rest_framework import serializers
from .models import *
from rest_framework.exceptions import ValidationError
from django.db.models import Q



class WorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = '__all__'

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = '__all__'

    def create(self, validated_data):
        worker = validated_data.get('worker')
        date = validated_data.get('date')
        start_appointment = validated_data.get('start')
        end_appointment = validated_data.get('end')
        schedule = Schedule.objects.order_by('start').filter(worker=worker).filter(date=date)
        for appointment in schedule:
            
            start, end = appointment.start, appointment.end
            print(start,end)
            print(start_appointment, end_appointment)
            if start_appointment >= start and start_appointment <= end:
                raise ValidationError('Busy time!')
            if end_appointment >= end and end_appointment <= end:
                raise ValidationError('Busy time!')
        return Schedule.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        worker = instance.worker
        date = validated_data.get('date')
        location = validated_data.get('location')
        start_appointment = validated_data.get('start')
        end_appointment = validated_data.get('end')
        schedule = Schedule.objects.order_by('start').filter(worker=worker).filter(date=date).filter(location=location).filter(~Q(id=instance.id))
        for appointment in schedule:
            start, end = appointment.start, appointment.end
            if start_appointment >= start and start_appointment <= end:
                raise ValidationError('Busy time!')
            if end_appointment >= end and end_appointment <= end:
                raise ValidationError('Busy time!')
        return super().update(instance, validated_data)
        

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'

    def create(self, validated_data):
        date = validated_data.get('date')
        start_appointment = validated_data.get('start')
        end_appointment = validated_data.get('end')
        worker = validated_data.get('worker')
        location = validated_data.get('location')
        schedule = Schedule.objects.order_by('start').filter(worker=worker).filter(date=date)

        for appointment in schedule:
            start, end = appointment.start, appointment.end
            if start_appointment >= start and start_appointment <= end:
                raise ValidationError('Busy time!')
            if end_appointment >= end and end_appointment <= end:
                raise ValidationError('Busy time!')

        Schedule.objects.create(worker=worker, date=date, start=start_appointment, end=end_appointment, location=location)
        return Appointment.objects.create(**validated_data)
    
