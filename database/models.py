import datetime

from django.db import models
from django.utils import timezone
from django.utils.timezone import now
from .validators import banned_words
from django.contrib.auth.models import User

class Caretaker(models.Model):
    caretakerUser = models.OneToOneField(User, on_delete=models.CASCADE, default=1) 
    listedPatients = models.JSONField() 

class Patient(models.Model):
    patientUser = models.OneToOneField(User, on_delete=models.CASCADE, default=1)

class Requests(models.Model):
    request_type = models.CharField(max_length=30)
    request_specification = models.CharField(max_length=30)
    request_patient = models.OneToOneField(User, on_delete=models.CASCADE, default=1)
    request_time = models.DateTimeField('Time Created',default=now, editable=False)

    def date_created(self):
        current_datetime = dt.datetime.now()
        current_time = (current_datetime.hour + ":" + current_datetime.minute + ":" + current_datetime.second)
        return self.request_time = current_time