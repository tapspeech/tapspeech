from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.core.window import Window
Window.size = (360, 640)
Window.clearcolor = (1, 1, 1, 1)

kv = Builder.load_file("caretaker.kv")
readCsv = open("/Users/huang/Desktop/Tapspeech/csv - Sheet1.csv").read()
patientList = readCsv.split(',')
global pos
pos = [0, 1055]

class Patient(App, BoxLayout):
    def build(self):
        for patient in patientList:
            return Button(text = str(patient), background_color=(1,1,1,1), pos=pos, size_hint = (.25, .18))
            pos[0] += 400

Patient().run()
