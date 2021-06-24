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


'''
this below line returns an error, im commenting it out until you fix it
layout = GridLayout(cols=2)
'''

class start_Window(Screen):
    def build(self):
        btn = Button(text ="Push Me !",
                     background_normal = 'images',
                     background_down = 'down.png',
                     size_hint = (.3, .3),
                     pos_hint = {"x":0.35, "y":0.3}
                   )
        btn.bind(on_press = self.callback)
        return btn

class login_Window(Screen):
    birthday = ObjectProperty(None)
    name = ObjectProperty(None)
    def validate(self):
        # validating if the email already exists
        if ReadSQL.check_email(self.email.text) == False:
            popFun(1)
        else:
            # switching the current screen to display validation result
            sm.current = 'english'

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
    pass

# Runs the kv file

kv = Builder.load_file("tapSpeech.kv")

class tapSpeechApp(App):
    Window.clearcolor = (0.88,0.92,0.92,1)
    def build(self):
        return kv

if __name__ == '__main__':
    tapSpeechApp().run()
    self.root.current = 'register_Window'
