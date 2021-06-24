# import all the relevant classes
import pandas as pd
from plyer import battery, tts, vibrator
from validate_email import validate_email
import sqlite3
import os

import django
#os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tapSpeech.settings')
#django.setup()

#from tapSpeech_app.models import Patient, Caretaker, Requests

from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.layout import Layout
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
import pandas as pd
from plyer import battery, tts, vibrator
from kivy.uix.gridlayout import GridLayout

from kivy.core.text import LabelBase
from kivy.core.audio import SoundLoader
from kivy.core.window import Window

Window.size = (360, 640)

LabelBase.register(name='GalanoGrotesque', fn_regular='GalanoGrotesque.otf')
#LabelBase.register(name='Pacifico', fn_regular='Pacifico.tff')

#location = 'start_Window'

'''
this below line returns an error, im commenting it out until you fix it
layout = GridLayout(cols=2)
'''

class welcome(Screen):
#     def build(self):
#
#         # adding GridLayouts in App
#         # Defining number of coloumn and size of the buttons i.e height
#         layout = GridLayout(cols = 2, row_force_default = True,
#                             row_default_height = 30)
#
#         # 1st row
#         layout.add_widget(Button(text ='Hello 1', size_hint_x = None, width = 100))
#         layout.add_widget(Button(text ='World 1'))
#
#         # 2nd row
#         layout.add_widget(Button(text ='Hello 2', size_hint_x = None, width = 100))
#         layout.add_widget(Button(text ='World 2'))
#
#         # 3rd row
#         layout.add_widget(Button(text ='Hello 3', size_hint_x = None, width = 100))
#         layout.add_widget(Button(text ='World 3'))
#
#         # 4th row
#         layout.add_widget(Button(text ='Hello 4', size_hint_x = None, width = 100))
#         layout.add_widget(Button(text ='World 4'))
#
#         # returning the layout
#         return layout

#return welcome()

    '''
    def build(self):
        btn = Button(text ="Push Me !",
                     background_normal = 'images',
                     background_down = 'down.png',
                     size_hint = (.3, .3),
                     pos_hint = {"x":0.35, "y":0.3}
                   )
        btn.bind(on_press = self.callback)
        return btn
    '''

class login(Screen):
    birthday = ObjectProperty(None)
    name = ObjectProperty(None)

    def check_info(name, birthday):
        test = ReadSQL('db.sqlite3')
        df = test.query_columns_to_dataframe('tapSpeech_app_patient', ['patientFullName'])
        df2 = test.query_columns_to_dataframe('tapSpeech_app_patient', ['patientBirthday'])
        for number in range(len(df.index)):
            if name == df.at[number,'patientFullName']:
                if birthday == df2.at[number, 'patientBirthday']:
                    return True
            return False

    def check_info_caretaker(name, password):
        test = ReadSQL('db.sqlite3')
        df = test.query_columns_to_dataframe('tapSpeech_app_caretaker', ['caretakerFullName'])
        df2 = test.query_columns_to_dataframe('tapSpeech_app_caretaker', ['caretakerPassword'])
        for number in range(len(df.index)):
            if name == df.at[number,'caretakerFullName']:
                if password == df2.at[number, 'caretakerPassword']:
                    return True
            return False

    def validate(self):
        # validating if the info already exists
        if ReadSQL.check_info(self.name.text, self.name.birthday) == False:
            popFun(1)
        else:
            # switching the current screen to display validation result
            sm.current = 'Patient_Up'

            # reset TextInput widget
            self.name.text = ""
            self.birthday.text = ""

class register(Screen):
    birthday = ObjectProperty(None)
    name = ObjectProperty(None)

    def backbtn(self):
        sm.current="login"

    def signupbtnp(self):
        # for patient
        # creating a DataFrame of the info
        user = pd.DataFrame([[self.name.text, self.birthday.text, "patient"]],
                            columns = ['Name', 'Birthdate', 'User Type'])
        if self.name.text != "":
            if(check_info(self.name.text, self.birthday.text)):
                if self.name.text not in users['Name'].unique():
                    # if email does not exist already then append to the csv file
                    # change current screen to log in the user now
                    user.to_csv('login.csv', mode = 'a', header = False, index = False)
                    # uses the FullName, Email and Password to create a new listing under the 'Patient' class
                    new_patient = Patient(patientFullName = self.name.text, patientBirthDate = self.birthday.text)
                    new_patient.save()
                    sm.current = 'login_Window'
                    self.name.text = ""
                    self.birthday.text = ""
                else:
                    popFun(2)
            else:
                    # if email invalid
                popFun(3)
        else:
                # if values are empty or invalid show pop up
            popFun(1)

    def signupbtnc(self):
        # for caretaker
        # creating a DataFrame of the info
        user = pd.DataFrame([[self.name.text, self.pwd.text, "caretaker"]],
                            columns = ['Name', 'Password', 'User Type'])
        if self.name.text != "":
            if(check_info_caretaker(self.name.text, self.pwd.text)):
                if self.name.text not in users['Name'].unique():
                    # if email does not exist already then append to the csv file
                    # change current screen to log in the user now
                    user.to_csv('login.csv', mode = 'a', header = False, index = False)
                    new_caretaker = Caretaker(caretakerFullName = self.name.text, caretakerPassword = self.pwd.text)
                    new_caretaker.save()
                    sm.current = 'login'
                    self.name.text = ""
                    self.pwd.text = ""
                else:
                    popFun(2)
            else:
                # if email invalid
                popFun(3)
        else:
            # if values are empty or invalid show pop up
            popFun(1)

class Patient_Up(Screen):
    pass

class Patient_Down(Screen):
    pass

class Contacts(Screen):
    pass

class Caretaker(Screen):
    pass

class WindowManager(ScreenManager):
    #welcome_Window = ObjectProperty()
    pass

# Runs the kv file

kv = Builder.load_file("tapSpeech.kv")
sm = ScreenManager()


class tapSpeechApp(App):
    Window.clearcolor = (0.88,0.92,0.92,1)
    WindowManager.current = "login"
    def build(self):
        return kv

if __name__ == '__main__':
    tapSpeechApp().run()
