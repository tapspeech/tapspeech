import datetime

from django.db import models
from django.utils import timezone
from django.utils.timezone import now
from django.contrib.auth.models import User

class Caretaker(models.Model):
    caretakerFullName = models.CharField(max_length=30, default = '')
    caretakerEmail = models.CharField(max_length=30, default = '')
    caretakerPassword = models.CharField(max_length=30, default = '')
    listedPatients = models.JSONField()

class Patient(models.Model):
    patientFullName = models.CharField(max_length=30, default = '')
    patientBirthDate = models.CharField(max_length=30, default = '')
    patientEmergencyContact = models.CharField(max_length=30, default = '')
    patientEmergencyContact2 = models.CharField(max_length=30, default = '')
    patientEmergencyContact3 = models.CharField(max_length=30, default = '')

    def __str__(self):
        return self.patientFullName

class Requests(models.Model):
    request_type = models.CharField(max_length=30)
    request_specification = models.CharField(max_length=30)
    request_patient = models.CharField(max_length=30, default = '')
    request_time = models.DateTimeField('Time Created',default=now, editable=False)

    def date_created(self):
        current_datetime = dt.datetime.now()
        current_time = (current_datetime.hour + ":" + current_datetime.minute + ":" + current_datetime.second)
        return self.request_time == current_time
