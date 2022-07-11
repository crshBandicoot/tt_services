from rest_framework import serializers
from .models import *
from rest_framework.exceptions import ValidationError
from django.db.models import Q
from datetime import datetime, timedelta

class SpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialization
        fields = '__all__'


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
        fields = ('id', 'date', 'start', 'end', 'worker')

    def create(self, validated_data):
        worker = validated_data.get('worker')
        date = validated_data.get('date')
        location = validated_data.get('location')
        start_appointment = validated_data.get('start')
        end_appointment = validated_data.get('end')
        schedule = Schedule.objects.order_by('start').filter(worker=worker).filter(date=date).filter(location=location)
        for appointment in schedule:
            start, end = appointment.start, appointment.end
            if start_appointment >= start and start_appointment <= end_appointment:
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
            if start_appointment >= start and start_appointment <= end_appointment:
                raise ValidationError('Busy time!')
            if end_appointment >= end and end_appointment <= end:
                raise ValidationError('Busy time!')
        return super().update(instance, validated_data)
        

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ('id', 'client', 'date', 'start', 'procedure')

    def create(self, validated_data):
        date = validated_data.get('date')
        start_appointment = validated_data.get('start')
        procedure = validated_data.get('procedure')
        worker = Worker.objects.get(specialization=procedure)
        start_date = datetime(1,1,1, start_appointment.hour, start_appointment.minute)
        end_appointment = (start_date + timedelta(hours=1)).time()
        schedule = Schedule.objects.order_by('start').filter(worker=worker).filter(date=date)

        for appointment in schedule:
            start, end = appointment.start, appointment.end
            if start_appointment >= start and start_appointment <= end_appointment:
                raise ValidationError('Busy time!')
            if end_appointment >= end and end_appointment <= end:
                raise ValidationError('Busy time!')

        Schedule.objects.create(worker=worker, date=date, start=start_appointment, end=end_appointment, location=None)
        return Appointment.objects.create(**validated_data)
    
