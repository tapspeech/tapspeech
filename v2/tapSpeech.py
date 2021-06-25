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
def popFun(type):
    if type == 1:
        label_content="Please enter valid information"
    elif type == 2:
        label_content="Account already exists"
    elif type == 3:
        label_content="Please enter a valid email"

    window = Popup(title='Error',
    content=Label(text=label_content),
    size_hint=(None, None), size=(500, 300))

    window.open()

class en_welcomeScreen(Screen):
    pass

class ReadSQL:
    def __init__(self, database):
        self.database = database
        self.conn = sqlite3.connect(self.database)
        self.cur = self.conn.cursor()

    def query_columns_to_dataframe(self, table, columns):
        query = 'select '
        for i in range(len(columns)):
            query = query + columns[i] + ', '
        query = query[:-2] + ' from ' + table
        #~ print(query)
        df = pd.read_sql_query(query, self.conn)
        return df

    def check_info_patient(name, birthday):
        #list to store emails
        names=[]
        birthdays=[]
        namecheck = False
        birthdatecheck = False
        accountexists = False
        #selects the database
        test = ReadSQL('db.sqlite3')
        df = test.query_columns_to_dataframe('tapSpeech_app_patient', ['patientFullName'])
        df2 = test.query_columns_to_dataframe('tapSpeech_app_patient', ['patientBirthDate'])
        #adds all emails into the emails list
        for number in range(len(df.index)):
            names.append(df.at[number,'patientFullName'])
        for number2 in range(len(df2.index)):
            birthdays.append(df2.at[number2,'patientBirthDate'])
        #returns true if the email exists and false if it does not
        for i in range(len(names)):
            if name == names[i]:
                namecheck = True
                if birthday == birthdays[i]:
                    birthdatecheck = True
                    if namecheck and birthdatecheck == True:
                        accountexists = True
                        return accountexists
                else:
                    return accountexists
            else:
                return accountexists

class en_loginScreen(Screen):
    username = ObjectProperty(None)
    password = ObjectProperty(None)

    def validate(self):
        # validating if the info already exists
        # if ReadSQL.check_info(self.username.text, self.password.text) == False:
        if (not self.username.text) or (not self.password.text):
            popFun(1)
        else:
            App.get_running_app().sm.current = 'en_patientUp'

class en_registerScreen(Screen):
    birthday = ObjectProperty(None)
    name = ObjectProperty(None)

    def signupbtnc(self):
        # for caretaker
        # creating a DataFrame of the info
        user = pd.DataFrame([[self.name.text, self.birthday.text, "caretaker"]],
                            columns = ['Name', 'Password', 'User Type'])
        if self.name.text != "":
            resp = ReadSQL.check_info_patient(self.name.text, self.birthday.text)
            if resp == False:
                new_patient = Patient(patientFullName = self.name.text, patientBirthDate = self.birthday.text)
                new_patient.save()
                sm.current = 'login'
                self.name.text = ""
                self.birthday.text = ""
            else:
                # if email is already made
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
        self.sm = windowManager(transition=FadeTransition())

        self.sm.add_widget(en_welcomeScreen(name="en_welcome"))
        self.sm.add_widget(en_loginScreen(name="en_login"))
        self.sm.add_widget(en_registerScreen(name="en_register"))
        self.sm.add_widget(en_patientUpScreen(name="en_patientUp"))
        self.sm.add_widget(en_patientDownScreen(name="en_patientDown"))
        self.sm.add_widget(en_contactsScreen(name="en_contacts"))
        self.sm.add_widget(en_caretakerScreen(name="en_caretaker"))

        self.sm.add_widget(ct_welcomeScreen(name="ct_welcome"))
        self.sm.add_widget(ct_loginScreen(name="ct_login"))
        self.sm.add_widget(ct_registerScreen(name="ct_register"))
        self.sm.add_widget(ct_patientUpScreen(name="ct_patientUp"))
        self.sm.add_widget(ct_patientDownScreen(name="ct_patientDown"))
        self.sm.add_widget(ct_contactsScreen(name="ct_contacts"))
        self.sm.add_widget(ct_caretakerScreen(name="ct_caretaker"))
        self.sm.current = "en_welcome"
        return self.sm

if __name__ == '__main__':
    tapSpeechApp().run()
