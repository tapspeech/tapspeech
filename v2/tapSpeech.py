# import all the relevant classes
import pandas as pd
from plyer import battery, tts, vibrator
from validate_email import validate_email
import sqlite3
import os

import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tapSpeech.settings')
django.setup()

from tapSpeech_app.models import Patient, Caretaker, Requests
from kivy.uix.carousel import Carousel
from kivy.uix.image import AsyncImage

from datetime import datetime
import pytz
from kivy.app import App
from kivy.lang import Builder
from kivy.core.text import LabelBase
from kivy.core.audio import SoundLoader
from kivy.core.window import Window

from kivy.properties import ObjectProperty, StringProperty

from kivy.uix.layout import Layout
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition, SlideTransition
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
LabelBase.register(name='Noto', fn_regular='NotoSans.otf')

global_patient_name = ''

def error(type):
    if type == 1:
        label_content="Please enter valid information"
    elif type == 2:
        label_content="Account already exists"
    elif type == 3:
        label_content="Incomplete Function"

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
        #lists to store names and birthdays
        names=[]
        birthdays=[]
        namecheck = False
        birthdatecheck = False
        accountexists = False
        #selects the database
        test = ReadSQL('db.sqlite3')
        df = test.query_columns_to_dataframe('tapSpeech_app_patient', ['patientFullName'])
        df2 = test.query_columns_to_dataframe('tapSpeech_app_patient', ['patientBirthDate'])
        #adds all names and birthday into the emails list
        for number in range(len(df.index)):
            names.append(df.at[number,'patientFullName'])
        for number2 in range(len(df2.index)):
            birthdays.append(df2.at[number2,'patientBirthDate'])
        #returns true if the names and birthday exists and false if it does not
        for i in range(len(names)):
            if name == names[i]:
                namecheck = True
            if birthday == birthdays[i]:
                birthdatecheck = True
        if namecheck and birthdatecheck == True:
            accountexists = True
        return accountexists

    def check_info_caretaker(name, password):
        #list to store emails
        names=[]
        passwords=[]
        namecheck = False
        passwordcheck = False
        accountexists = False
        #selects the database
        test = ReadSQL('db.sqlite3')
        df = test.query_columns_to_dataframe('tapSpeech_app_caretaker', ['caretakerFullName'])
        df2 = test.query_columns_to_dataframe('tapSpeech_app_caretaker', ['caretakerPassword'])
        #adds all emails into the emails list
        for number in range(len(df.index)):
            names.append(df.at[number,'caretakerFullName'])
        for number2 in range(len(df2.index)):
            passwords.append(df2.at[number2,'caretakerPassword'])
        #returns true if the email exists and false if it does not
        for i in range(len(names)):
            if name == names[i]:
                namecheck = True
            if password == passwords[i]:
                passwordcheck = True
        if namecheck and passwordcheck == True:
            accountexists = True
        return accountexists

class en_loginScreen(Screen):
    username = ObjectProperty(None)
    password = ObjectProperty(None)

    def check_for_login(self, username, password):
        is_caretaker = False
        is_patient = False

        is_caretaker = ReadSQL.check_info_caretaker(self.username.text, self.password.text)
        if is_caretaker == False:
            is_patient = ReadSQL.check_info_patient(self.username.text, self.password.text)
        if is_caretaker == True:
            return 'caretaker'
        if is_patient == True:
            return 'patient'
        if is_caretaker and is_patient == False:
            return 'role not assigned'

    def validate(self):
        # error 1 - check if they've input something
        if (not self.username.text) or (not self.password.text):
            error(1)
        # error 2 - check if account already exists
        else:
            completed_login = self.check_for_login(self.username.text, self.password.text)
            if completed_login == 'none':
                error(1)
            else:
                if completed_login == 'patient':
                    App.get_running_app().sm.current = 'en_patientUp'
                    global global_patient_name
                    global_patient_name = self.username.text
                elif completed_login == 'caretaker':
                    App.get_running_app().sm.current = 'en_caretakerUp'

                    '''
                    I dont know what the two lines,
                    remove this comment if those lines are necessary
                    '''

                    global global_caretaker_name
                    global_caretaker_name = self.username.text

class en_registerScreen(Screen):
    username = ObjectProperty(None)
    password = ObjectProperty(None)

    def register_user(self, user_type):
        return_data = [self.username.text, self.password.text, user_type]
        print(return_data)
        completed_registration = False
        # if the user_type is equal to patient, run the function to add to patient database
        if user_type == 'patient':
            infocheckresult = ReadSQL.check_info_patient(self.username.text, self.password.text)
            if infocheckresult == False:
                # if infocheckresult is False, it means that they are not registered in the database and can be added
                new_patient = Patient(patientFullName = self.username.text, patientBirthDate = self.password.text)
                new_patient.save()
                completed_registration = True
                return completed_registration
            else:
                # if infocheckresult is True, it means that they are already registered in the database and can't be added, return an error
                completed_registration = False
                return completed_registration
        # if the user_type is NOT equal to patient (which means they are caretaker), run the function to add to caretaker database
        else:
            infocheckresult = ReadSQL.check_info_caretaker(self.username.text, self.password.text)
            if infocheckresult == False:
                # if infocheckresult is False, it means that they are not registered in the database and can be added
                new_caretaker = Caretaker(caretakerFullName = self.username.text, caretakerPassword = self.password.text, listedPatients = '')
                new_caretaker.save()
                completed_registration = True
                return completed_registration
            else:
                # if infocheckresult is True, it means that they are already registered in the database and can't be added, return an error
                completed_registration = False
                return completed_registration

    def validate(self, user_type):
        # error 1 - check if they've input something
        if (not self.username.text) or (not self.password.text):
            error(1)
        # error 2 - check if account already exists
        # else if ReadSQL.check_info(self.username.text, self.password.text) == False:
        #   error(2)
        else:
            completed_registration = self.register_user(user_type)
            if completed_registration == False:
                error(1)
            else:
                if user_type == 'patient':
                    App.get_running_app().sm.current = 'en_patientUp'
                    global global_patient_name
                    global_patient_name = self.username.text
                elif user_type == 'caretaker':
                    print('running')
                    App.get_running_app().sm.current = 'en_caretakerUp'

                    '''
                    I dont know what the two lines,
                    remove this comment if those lines are necessary
                    '''

                    global global_caretaker_name
                    global_caretaker_name = self.username.text
                else:
                    print('running error')
                    error(3)

class en_patientUpScreen(Screen):
    say_something = ObjectProperty(None)
    hello_name = ObjectProperty(None)

    def sound_alarm(self):
        self.sound = SoundLoader.load(os.path.join('audio','ios_ringtone.mp3'))
        self.sound.play()

    def textInput_enter(self):
        message = self.say_something.text
        self.say_something.text = ''
        tts.speak(message)

    def change_helloMessage(self):
        global global_patient_name
        self.hello_name.text = 'Hello, '+global_patient_name

    def contact_info(type):

        window = Popup(title='',
        content=Label(text='Emergency Contact Number:'),
        size_hint=(None, None), size=(500, 300))

        window.open()

class en_patientDownScreen(Screen):
    dots = ObjectProperty(None)
    label_1 = ObjectProperty(None)
    label_2 = ObjectProperty(None)
    label_3 = ObjectProperty(None)
    label_4 = ObjectProperty(None)

    request_specification = ''
    request_type = 'Liquid'

    # the message below is what you want to be sent to the caretaker
    def returnMessage(self,label_id):
        global global_patient_name
        if label_id == 'label_1':
            message = self.label_1.text
        elif label_id == 'label_2':
            message = self.label_2.text
        elif label_id == 'label_3':
            message = self.label_3.text
        elif label_id == 'label_4':
            message = self.label_4.text
        else:
            pass

        now = datetime.now()
        tz_HK = pytz.timezone('Hongkong')
        datetime_HK = datetime.now(tz_HK)
        current_time = datetime_HK.strftime("%H:%M:%S")
        print(message + " " + self.request_type)
        new_request = Requests(request_type = self.request_type, request_specification = message, request_patient = global_patient_name, request_time = current_time)
        new_request.save()
        print(new_request)

    def changebuttons(self,index_no):
        # drinks menu
        if index_no == 'slide #0':
            self.label_1.text = 'Water'
            self.label_2.text = 'Milk'
            self.label_3.text = 'Juice'
            self.label_4.text = 'Tea'
            self.dots.source = 'images/icons/general/dots_1.png'
            self.request_type = 'Liquid'
        # food menu
        elif index_no == 'slide #1':
            self.label_1.text = 'Rice'
            self.label_2.text = 'Noodles'
            self.label_3.text = 'Soup'
            self.label_4.text = 'Bread'
            self.dots.source = 'images/icons/general/dots_2.png'
            self.request_type = 'Food'
        # food menu
        elif index_no == 'slide #2':
            self.label_1.text = 'Poop'
            self.label_2.text = 'Urinate'
            self.label_3.text = 'Feeling Unwell'
            self.label_4.text = 'Other'
            self.dots.source = 'images/icons/general/dots_3.png'
            self.request_type = 'Toilet'
        # food menu
        elif index_no == 'slide #3':
            self.label_1.text = 'Up'
            self.label_2.text = 'Down'
            self.label_3.text = 'Get On'
            self.label_4.text = 'Get Off'
            self.dots.source = 'images/icons/general/dots_4.png'
            self.request_type = 'Bed'

class en_contactsScreen(Screen):
    pass

class en_informationScreen(Screen):
    pass

class en_caretakerUpScreen(Screen):
    caretaker_name = ObjectProperty(None)

    def display_caretaker_name(self):
        global global_caretaker_name
        self.caretaker_name.text = 'Caretaker: '+global_caretaker_name

class en_caretakerDownScreen(Screen):
    pass


class en_informationScreen(Screen):
    pass

class ct_welcomeScreen(Screen):
    pass

class ct_loginScreen(Screen):
    pass

class ct_registerScreen(Screen):
    pass

class ct_patientUpScreen(Screen):
    say_something = ObjectProperty(None)

    def sound_alarm(self):
        self.sound = SoundLoader.load(os.path.join('audio','ios_ringtone.mp3'))
        self.sound.play()

    def textInput_enter(self):
        message = self.say_something.text
        self.say_something.text = ''
        tts.speak(message)

class ct_patientDownScreen(Screen):
    dots = ObjectProperty(None)
    label_1 = ObjectProperty(None)
    label_2 = ObjectProperty(None)
    label_3 = ObjectProperty(None)
    label_4 = ObjectProperty(None)

    # the message below is what you want to be sent to the caretaker
    def returnMessage(self,label_id):
        if label_id == 'label_1ct':
            message = self.label_1.text
        elif label_id == 'label_2ct':
            message = self.label_2.text
        elif label_id == 'label_3ct':
            message = self.label_3.text
        elif label_id == 'label_4ct':
            message = self.label_4.text
        else:
            pass
        print(message)

    def changebuttons(self,index_no):
        # drinks menu
        if index_no == 'slide #0':
            self.label_1.text = '水'
            self.label_2.text = '牛奶'
            self.label_3.text = '果汁'
            self.label_4.text = '茶'
            self.dots.source = 'images/icons/general/dots_1.png'
        # food menu
        elif index_no == 'slide #1':
            self.label_1.text = '米飯'
            self.label_2.text = '麵'
            self.label_3.text = '湯'
            self.label_4.text = '麵包'
            self.dots.source = 'images/icons/general/dots_2.png'
        # food menu
        elif index_no == 'slide #2':
            self.label_1.text = "o'屎"
            self.label_2.text = "o'尿"
            self.label_3.text = '感到不舒服'
            self.label_4.text = '其他'
            self.dots.source = 'images/icons/general/dots_3.png'
        # food menu
        elif index_no == 'slide #3':
            self.label_1.text = '上'
            self.label_2.text = '下'
            self.label_3.text = '上床'
            self.label_4.text = '下床'
            self.dots.source = 'images/icons/general/dots_4.png'

class en_contactsScreen(Screen):
    pass

class ct_contactsScreen(Screen):
    pass

class ct_caretakerUpScreen(Screen):
    pass

class ct_caretakerDownScreen(Screen):
    pass

class windowManager(ScreenManager):
    pass

class tapSpeechApp(App):
    #kv = Builder.load_file("tapSpeech.kv")
    #Window.clearcolor = (0.88,0.92,0.92,1)
    Window.clearcolor = (1,1,1,1)

    def build(self):
        # Bear witness to Matthew's sexy code below
        self.sm = windowManager()

        self.sm.add_widget(en_welcomeScreen(name="en_welcome"))
        self.sm.add_widget(en_loginScreen(name="en_login"))
        self.sm.add_widget(en_registerScreen(name="en_register"))
        self.sm.add_widget(en_patientUpScreen(name="en_patientUp"))
        self.sm.add_widget(en_patientDownScreen(name="en_patientDown"))
        self.sm.add_widget(en_contactsScreen(name="en_contacts"))
        self.sm.add_widget(en_caretakerUpScreen(name="en_caretakerUp"))
        self.sm.add_widget(en_caretakerDownScreen(name="en_caretakerDown"))
        self.sm.add_widget(en_informationScreen(name="en_information"))
        self.sm.add_widget(ct_welcomeScreen(name="ct_welcome"))
        self.sm.add_widget(ct_loginScreen(name="ct_login"))
        self.sm.add_widget(ct_registerScreen(name="ct_register"))
        self.sm.add_widget(ct_patientUpScreen(name="ct_patientUp"))
        self.sm.add_widget(ct_patientDownScreen(name="ct_patientDown"))
        self.sm.add_widget(ct_contactsScreen(name="ct_contacts"))
        self.sm.add_widget(ct_caretakerUpScreen(name="ct_caretakerUp"))
        self.sm.add_widget(ct_caretakerDownScreen(name="ct_caretakerDown"))
        self.sm.current = "en_welcome"
        return self.sm

if __name__ == '__main__':
    tapSpeechApp().run()
