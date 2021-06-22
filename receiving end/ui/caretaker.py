from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.core.window import Window

Window.size = (640, 360)
Window.clearcolor = (1, 1, 1, 1)

kv = Builder.load_file("caretaker.kv")

def update_patients_list():
    global patient_list

    patient_database = open('caretaker.csv', 'r')
    patient_list = patient_database.read()
    patient_database.close()
    patient_list = patient_list.split('\n')

    new_patient_list = []
    for x in patient_list:
        individual_patient = x.split(',')
        new_patient_list.append(individual_patient)

    patient_list = new_patient_list
    return patient_list

update_patients_list()
print(patient_list)

'''
class Patient(App, BoxLayout):
    def build(self):
        for patient in patientList:
            return Button(text = str(patient), background_color=(1,1,1,1), pos=pos, size_hint = (.25, .18))
            pos[0] += 400
'''

class caretakerApp(App):
    def build(self):
        return kv

if __name__ == '__main__':
    caretakerApp().run()
