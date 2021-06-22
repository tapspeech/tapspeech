import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tapSpeech.settings')
django.setup()

from tapSpeech_app.models import Patient

x = input("input name pls")
y = input("input email pls")
z = input("input password pls")

new_patient = Patient(patientFullName = x, patientEmail = y, patientPassword = z)
new_patient.save()
