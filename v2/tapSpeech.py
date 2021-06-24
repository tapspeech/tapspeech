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

from kivy.core.text import LabelBase
from kivy.core.audio import SoundLoader
from kivy.core.window import Window

Window.size = (360, 640)

LabelBase.register(name='GalanoGrotesque', fn_regular='GalanoGrotesque.otf')

#location = 'start_Window'

'''
this below line returns an error, im commenting it out until you fix it
layout = GridLayout(cols=2)
'''

class start_Window(Screen):
    pass
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

class login_Window(Screen):
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
            sm.current = 'Patient_Window_Up'

            # reset TextInput widget
            self.email.text = ""
            self.pwd.text = ""



class register_Window(Screen):
    pass

class Patient_Window_Up(Screen):
    pass

class Patient_Window_Down(Screen):
    pass

class Contacts_Window(Screen):
    pass

class Caretaker_Window(Screen):
    pass

class WindowManager(ScreenManager):
    start_Window = ObjectProperty()
    pass

# Runs the kv file

kv = Builder.load_file("tapSpeech.kv")

class tapSpeechApp(App):
    Window.clearcolor = (0.88,0.92,0.92,1)
    def build(self):
        '''
        self.root = WindowManager()
        self.auth()
        '''
        return kv

    '''
    def auth(self):
        global location
        if location == 'start_Window':
            print('works')
            self.root.current = 'start_Window'
    '''

if __name__ == '__main__':
    tapSpeechApp().run()
