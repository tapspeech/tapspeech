from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.core.window import Window

from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivymd.uix.list import MDList, TwoLineListItem
from kivy.uix.scrollview import ScrollView

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

class caretakerApp(MDApp):
    def build(self):
        screen = Screen()

        scroll = ScrollView()
        list_view = MDList()
        scroll.add_widget(list_view)

        for patient in patient_list:
            items = TwoLineListItem(text=str(patient[0]), secondary_text=str(patient[1]))
            list_view.add_widget(items)

        '''
        item1 = TwoLineListItem(text='Item 1', secondary_text='wo xiang si')
        item2 = TwoLineListItem(text='Item 2', secondary_text='wo hai xiang si')

        list_view.add_widget(item1)
        list_view.add_widget(item2)
        '''

        screen.add_widget(scroll)
        return screen
        #return kv

if __name__ == '__main__':
    caretakerApp().run()
