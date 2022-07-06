from django.db import models

class Specialization(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name

class Location(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name

class Worker(models.Model):
    name = models.CharField(max_length=255)
    specialization = models.ForeignKey(Specialization, on_delete=models.SET_NULL, null=True)
    location = models.OneToOneField(Location, on_delete=models.SET_NULL, null=True)
    job_start = models.TimeField()
    job_end = models.TimeField()
    def __str__(self):
        return str(self.specialization) + ' - ' + str(self.name) + ' ' + self.job_start.strftime('%H:%M-') + self.job_end.strftime('%H:%M')

class Schedule(models.Model):
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    client = models.CharField(max_length=255)
    date = models.DateField()
    start = models.TimeField()
    end = models.TimeField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.date.strftime('%d %b %Y') + self.start.strftime(' %H:%M') + self.end.strftime('-%H:%M ') + str(self.worker.location) + ' - ' + self.worker.name

