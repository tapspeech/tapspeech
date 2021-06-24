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
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button

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

class welcomeScreen(Screen):
    layout = BoxLayout()

class loginScreen(Screen):
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

class registerScreen(Screen):
    birthday = ObjectProperty(None)
    name = ObjectProperty(None)

class patientUpScreen(Screen):
    pass

class patientDownScreen(Screen):
    pass

class contactsScreen(Screen):
    pass

class caretakerScreen(Screen):
    pass

class windowManager(ScreenManager):
    # start = ObjectProperty()
    pass

class tapSpeechApp(App):
    kv = Builder.load_file("tapSpeech.kv")
    Window.clearcolor = (0.88,0.92,0.92,1)

    def build(self):
        sm = windowManager()
        sm.add_widget(welcomeScreen(name="welcome"))
        sm.add_widget(loginScreen(name="login"))
        sm.add_widget(registerScreen(name="register"))
        sm.add_widget(patientUpScreen(name="patientUp"))
        sm.add_widget(patientDownScreen(name="patientDown"))
        sm.add_widget(contactsScreen(name="contacts"))
        sm.add_widget(caretakerScreen(name="caretaker"))

        sm.current = "welcome"
        return sm

if __name__ == '__main__':
    tapSpeechApp().run()
