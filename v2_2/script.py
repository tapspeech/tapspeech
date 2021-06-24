import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tapSpeech.settings')
django.setup()

from tapSpeech_app.models import Patient

x = input("input name pls")
y = input("input birthdate pls")
n = input("input emergency contact 1 pls")
n2 = input("input emergency contact 2 pls")
n3 = input("input emergency contact 3 pls")

new_patient = Patient(patientFullName = x, patientBirthDate = y, patientEmergencyContact = n, patientEmergencyContact2 = n2, patientEmergencyContact3 = n3)
new_patient.save()
