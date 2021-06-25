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
from kivy.core.text import LabelBase
from kivy.core.audio import SoundLoader
from kivy.core.window import Window

from kivy.properties import ObjectProperty, StringProperty

from kivy.uix.layout import Layout
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout

Window.size = (360, 760)

LabelBase.register(name='GalanoGrotesque', fn_regular='GalanoGrotesque.otf')
#LabelBase.register(name='Pacifico', fn_regular='Pacifico.tff')

#location = 'start'

'''
this below line returns an error, im commenting it out until you fix it
layout = GridLayout(cols=2)
'''

class en_welcomeScreen(Screen):
    pass

class en_loginScreen(Screen):
    birthday = ObjectProperty(None)
    name = ObjectProperty(None)
    password = ObjectProperty(None)

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
        if ReadSQL.check_info(self.name.text, self.birthday.text) == False:
            popFun(1)
        else:
            # switching the current screen to display validation result
            sm.current = 'Patient_Up'

            # reset TextInput widget
            self.name.text = ""
            self.birthday.text = ""

class en_registerScreen(Screen):
    birthday = ObjectProperty(None)
    name = ObjectProperty(None)

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
            if(check_info_patient(self.name.text, self.pwd.text)):
                if self.name.text not in users['Name'].unique():
                    # if email does not exist already then append to the csv file
                    # change current screen to log in the user now
                    user.to_csv('login.csv', mode = 'a', header = False, index = False)
                    new_caretaker = Caretaker(caretakerFullName = self.name.text, caretakerPassword = self.pwd.text)
                    new_caretaker.save()
                    sm.current = 'login'
                    self.name2.text = ""
                    self.pwd.text = ""
                else:
                    popFun(2)
            else:
                # if email invalid
                popFun(3)
        else:
            # if values are empty or invalid show pop up
            popFun(1)

class en_patientUpScreen(Screen):
    '''
    def __init__(self, **kwargs):
                # Change the 'name' from the line below to the username that is registered
                # Attach it to the database (in order to find the name)
                self.ids.Hello_Name.text = 'Hello, '+'name'
    #def on_start(self, **kwargs):
    '''


    def sound_alarm(self):
        self.sound = SoundLoader.load(os.path.join('audio','ios_ringtone.mp3'))
        self.sound.play()

class en_patientDownScreen(Screen):
    pass

class en_contactsScreen(Screen):
    pass

class en_caretakerScreen(Screen):
    pass

class ct_welcomeScreen(Screen):
    pass

class ct_loginScreen(Screen):
    pass

class ct_registerScreen(Screen):
    pass

class ct_patientUpScreen(Screen):
    pass

class ct_patientDownScreen(Screen):
    pass

class ct_contactsScreen(Screen):
    pass

class ct_caretakerScreen(Screen):
    pass

class windowManager(ScreenManager):
    pass

class tapSpeechApp(App):
    kv = Builder.load_file("tapSpeech.kv")
    #Window.clearcolor = (0.88,0.92,0.92,1)
    Window.clearcolor = (1,1,1,1)

    def build(self):
        # Bear witness to Matthew's sexy code below
        sm = windowManager(transition=FadeTransition())

        sm.add_widget(en_welcomeScreen(name="en_welcome"))
        sm.add_widget(en_loginScreen(name="en_login"))
        sm.add_widget(en_registerScreen(name="en_register"))
        sm.add_widget(en_patientUpScreen(name="en_patientUp"))
        sm.add_widget(en_patientDownScreen(name="en_patientDown"))
        sm.add_widget(en_contactsScreen(name="en_contacts"))
        sm.add_widget(en_caretakerScreen(name="en_caretaker"))

        sm.add_widget(ct_welcomeScreen(name="ct_welcome"))
        sm.add_widget(ct_loginScreen(name="ct_login"))
        sm.add_widget(ct_registerScreen(name="ct_register"))
        sm.add_widget(ct_patientUpScreen(name="ct_patientUp"))
        sm.add_widget(ct_patientDownScreen(name="ct_patientDown"))
        sm.add_widget(ct_contactsScreen(name="ct_contacts"))
        sm.add_widget(ct_caretakerScreen(name="ct_caretaker"))
        sm.current = "en_welcome"
        return sm

if __name__ == '__main__':
    tapSpeechApp().run()
