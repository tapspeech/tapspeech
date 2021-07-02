import datetime

from django.db import models
from django.utils import timezone
from django.utils.timezone import now
from django.contrib.auth.models import User

class Caretaker(models.Model):
    caretakerFullName = models.CharField(max_length=30, default = '')
    caretakerPassword = models.CharField(max_length=30, default = '')
    listedPatients = models.CharField(max_length=30, default = '')
    listedPatients2 = models.CharField(max_length=30, default = '')
    listedPatients3 = models.CharField(max_length=30, default = '')
    listedPatients4 = models.CharField(max_length=30, default = '')
    listedPatients5 = models.CharField(max_length=30, default = '')
    listedPatients6 = models.CharField(max_length=30, default = '')

class Patient(models.Model):
    patientFullName = models.CharField(max_length=30, default = '')
    patientBirthDate = models.CharField(max_length=30, default = '')
    # patientEmergencyContactName = models.CharField(max_length=30, default = '')
    patientEmergencyContact = models.CharField(max_length=30, default = '')
    # patientEmergencyContactName2 = models.CharField(max_length=30, default = '')
    patientEmergencyContact2 = models.CharField(max_length=30, default = '')
    # patientEmergencyContactName3 = models.CharField(max_length=30, default = '')
    patientEmergencyContact3 = models.CharField(max_length=30, default = '')
    patientMedicalHistory = models.TextField(max_length=5000, default = '')
    patientDiagnosis = models.TextField(max_length=5000, default = '' )
    patientMedication = models.TextField(max_length=5000, default = '')

    def __str__(self):
        return self.patientFullName

class Requests(models.Model):
    request_type = models.CharField(max_length=30)
    request_specification = models.CharField(max_length=30)
    request_patient = models.CharField(max_length=30, default = 'Untitled')
    request_time = models.CharField(max_length=30, default = '')
    request_date = models.CharField(max_length=30, default = '')
