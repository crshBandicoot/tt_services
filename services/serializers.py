from rest_framework import serializers
from .models import *
from rest_framework.exceptions import ValidationError
from django.db.models import Q

class SpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialization
        fields = '__all__'

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

class WorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = '__all__'

class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = ('id', 'client', 'date', 'start', 'end', 'worker')

    def create(self, validated_data):
        worker = validated_data.get('worker')
        date = validated_data.get('date')
        start_appointment = validated_data.get('start')
        end_appointment = validated_data.get('end')
        job_start = worker.job_start
        job_end = worker.job_end
        
        if validated_data.get('start') < job_start or validated_data.get('end') > job_end:
            raise ValidationError('Out of working hours!')

        appointments = Schedule.objects.order_by('start').filter(worker=worker).filter(date=date)
        busy = []
        for appointment in appointments:
            start, end = appointment.start, appointment.end
            busy.append((start, end))
        for i in busy:
            if start_appointment >= i[0] and start_appointment <= i[1]:
                raise ValidationError('Busy time!')
        for i in busy:
            if end_appointment >= i[0] and end_appointment <= i[1]:
                raise ValidationError('Busy time!')

        return Schedule.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        worker = instance.worker
        date = validated_data.get('date')
        start_appointment = validated_data.get('start')
        end_appointment = validated_data.get('end')
        job_start = worker.job_start
        job_end = worker.job_end
        if validated_data.get('start') < job_start or validated_data.get('end') > job_end:
            raise ValidationError('Out of working hours!')

        appointments = Schedule.objects.order_by('start').filter(worker=worker).filter(date=date).filter(~Q(id=instance.id))
        busy = []
        for appointment in appointments:
            start, end = appointment.start, appointment.end
            busy.append((start, end))
        for i in busy:
            if start_appointment >= i[0] and start_appointment <= i[1]:
                raise ValidationError('Busy time!')
        for i in busy:
            if end_appointment >= i[0] and end_appointment <= i[1]:
                raise ValidationError('Busy time!')

        return super().update(instance, validated_data)
        
    
