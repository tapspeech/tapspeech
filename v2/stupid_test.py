# import all the relevant classes
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

class welcome(Screen):
    pass

class Caretaker(Screen):
    pass

class WindowManager(ScreenManager):
    #welcome_Window = ObjectProperty()
    pass

# Runs the kv file

kv = Builder.load_file("tapSpeech.kv")


class tapSpeechApp(App):
    Window.clearcolor = (0.88,0.92,0.92,1)
    def build(self):
        return kv

if __name__ == '__main__':
    tapSpeechApp().run()
