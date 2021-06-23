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

Window.size = (640, 360)
Window.clearcolor = (1,1,1,1)

location = 'English_Main'

# Message Function for English Text to Speech
speak_command_message = ''

# Message Function for Cantonese Audio Files
cantonese_message_name = ''

# resets all current request variables
curr_request_type = ''
curr_request_specification = ''
curr_request_patient = ''

# class to call the popup function
class PopupWindow(Widget):
    def btn(self):
        popFun(1)

# class to build GUI for a popup window
class P(FloatLayout):
    pass

# function that displays the content
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
    #detects whether the email given as the parameter exists
    def check_email(email):
        #list to store emails
        emails=[]
        #selects the database
        test = ReadSQL('db.sqlite3')
        df = test.query_columns_to_dataframe('tapSpeech_app_patient', ['patientEmail'])
        df2 = test.query_columns_to_dataframe('tapSpeech_app_caretaker', ['caretakerEmail'])
        #adds all emails into the emails list
        for number in range(len(df.index)):
            emails.append(df.at[number,'patientEmail'])
        for number in range(len(df2.index)):
            emails.append(df2.at[number,'caretakerEmail'])
        #returns true if the email exists and false if it does not
        for i in range(len(emails)):
            if email == emails[i]:
                return True
        return False

# class to accept user info and validate it
class loginWindow(Screen):
    email = ObjectProperty(None)
    pwd = ObjectProperty(None)
    def validate(self):
        # validating if the email already exists
        if ReadSQL.check_email(self.email.text)==False:
            popFun()
        else:
            # switching the current screen to display validation result
            sm.current = 'english'

            # reset TextInput widget
            self.email.text = ""
            self.pwd.text = ""


# class to accept sign up info
class signupWindow(Screen):
    name2 = ObjectProperty(None)
    email = ObjectProperty(None)
    pwd = ObjectProperty(None)

    def backbtn(self):
        sm.current="login"

    def signupbtnc(self):
        # for caretaker
        # creating a DataFrame of the info
        user = pd.DataFrame([[self.name2.text, self.email.text, self.pwd.text, "caretaker"]],
                            columns = ['Name', 'Email', 'Password', 'User Type'])
        if self.email.text != "":
            if(validate_email(self.email.text)):
                if self.email.text not in users['Email'].unique():
                    # if email does not exist already then append to the csv file
                    # change current screen to log in the user now
                    user.to_csv('login.csv', mode = 'a', header = False, index = False)
                    new_caretaker = Caretaker(caretakerFullName = self.name2.text, caretakerEmail = self.email.text, caretakerPassword = self.pwd.text)
                    new_caretaker.save()
                    sm.current = 'login'
                    self.name2.text = ""
                    self.email.text = ""
                    self.pwd.text = ""
                else:
                    popFun(2)
            else:
                # if email invalid
                popFun(3)
        else:
            # if values are empty or invalid show pop up
            popFun(1)

    def signupbtnp(self):
        # for patient
        # creating a DataFrame of the info
        user = pd.DataFrame([[self.name2.text, self.email.text, self.pwd.text, "patient"]],
                            columns = ['Name', 'Email', 'Password', 'User Type'])
        if self.email.text != "":
            if(validate_email(self.email.text)):
                if self.email.text not in users['Email'].unique():
                    # if email does not exist already then append to the csv file
                    # change current screen to log in the user now
                    user.to_csv('login.csv', mode = 'a', header = False, index = False)
                    # uses the FullName, Email and Password to create a new listing under the 'Patient' class
                    new_patient = Patient(patientFullName = self.name2.text, patientEmail = self.email.text, patientPassword = self.pwd.text)
                    new_patient.save()
                    sm.current = 'login'
                    self.name2.text = ""
                    self.email.text = ""
                    self.pwd.text = ""
                else:
                    popFun(2)
            else:
                # if email invalid
                popFun(3)
        else:
            # if values are empty or invalid show pop up
            popFun(1)

# class to display validation result
class logDataWindow(Screen):
    pass

# class for managing screens
class windowManager(ScreenManager):
    pass

class English_Window(Screen):
    def change_menu(self, menu):
        global location
        location = menu
        if location == 'English_Main':
            self.ids.Thumb_label.text = 'Liquid'
            self.ids.Index_label.text = 'Toilet'
            self.ids.Middle_label.text = 'Food'
            self.ids.Pinky_label.text = 'Bed'
        elif location == 'English_Liquid':
            self.ids.Thumb_label.text = 'Exit'
            self.ids.Index_label.text = 'Water'
            self.ids.Middle_label.text = 'Juice'
            self.ids.Pinky_label.text = 'Milk'
        elif location == 'English_Toilet':
            self.ids.Thumb_label.text = 'Exit'
            self.ids.Index_label.text = 'Urinate'
            self.ids.Middle_label.text = 'Poop'
            self.ids.Pinky_label.text = 'Help'
        elif location == 'English_Food':
            self.ids.Thumb_label.text = 'Exit'
            self.ids.Index_label.text = 'Rice'
            self.ids.Middle_label.text = 'Pork'
            self.ids.Pinky_label.text = 'Chicken'
        elif location == 'English_Bed':
            self.ids.Thumb_label.text = 'Exit'
            self.ids.Index_label.text = 'Down'
            self.ids.Middle_label.text = 'Up'
            self.ids.Pinky_label.text = 'Help'
        else:
            pass

    def button_press(self, button):
        def change_speak_message(message):
            global speak_command_message
            speak_command_message = message

        def speak_message(message='speak_command'):
            if message == 'speak_command':
                global speak_command_message
                tts.speak(speak_command_message)
            else:
                tts.speak(message)

        def change_menu(menu):
            global location
            location = menu
            if location == 'English_Main':
                self.ids.Thumb_label.text = 'Liquid'
                self.ids.Index_label.text = 'Toilet'
                self.ids.Middle_label.text = 'Food'
                self.ids.Pinky_label.text = 'Bed'
            elif location == 'English_Liquid':
                self.ids.Thumb_label.text = 'Exit'
                self.ids.Index_label.text = 'Water'
                self.ids.Middle_label.text = 'Juice'
                self.ids.Pinky_label.text = 'Milk'
            elif location == 'English_Toilet':
                self.ids.Thumb_label.text = 'Exit'
                self.ids.Index_label.text = 'Urinate'
                self.ids.Middle_label.text = 'Poop'
                self.ids.Pinky_label.text = 'Help'
            elif location == 'English_Food':
                self.ids.Thumb_label.text = 'Exit'
                self.ids.Index_label.text = 'Rice'
                self.ids.Middle_label.text = 'Pork'
                self.ids.Pinky_label.text = 'Chicken'
            elif location == 'English_Bed':
                self.ids.Thumb_label.text = 'Exit'
                self.ids.Index_label.text = 'Down'
                self.ids.Middle_label.text = 'Up'
                self.ids.Pinky_label.text = 'Help'
            else:
                pass

        global location
        if button == 'Thumb':
            if location == 'English_Main':
                change_menu('English_Liquid')
                speak_message('Liquid selected')
                self.curr_request_type = 'Liquid 飲品'
            elif location == 'English_Liquid':
                change_menu('English_Main')
                speak_message('Exited liquid menu')
                change_speak_message('')
                self.curr_request_type = ''
                self.curr_request_specification = ''
            elif location == 'English_Toilet':
                change_menu('English_Main')
                speak_message('Exited toilet menu')
                change_speak_message('')
                self.curr_request_type = ''
                self.curr_request_specification = ''
            elif location == 'English_Food':
                change_menu('English_Main')
                speak_message('Exited food menu')
                change_speak_message('')
                self.curr_request_type = ''
                self.curr_request_specification = ''
            elif location == 'English_Bed':
                change_menu('English_Main')
                speak_message('Exited bed menu')
                change_speak_message('')
                self.curr_request_type = ''
                self.curr_request_specification = ''
            else:
                pass

        elif button == 'Index':
            if location == 'English_Main':
                change_menu('English_Toilet')
                speak_message('Toilet selected')
                self.curr_request_type = 'Toilet 廁所'
            elif location == 'English_Liquid':
                speak_message('Water')
                change_speak_message('Please give me some water')
                self.curr_request_specification = 'Water 水'
            elif location == 'English_Toilet':
                speak_message('Urinate')
                change_speak_message('I need to go urinate')
                self.curr_request_specification = 'Urinate o尿'
            elif location == 'English_Food':
                speak_message('Rice')
                change_speak_message('Please give me some rice')
                self.curr_request_specification = 'Rice 飯'
            elif location == 'English_Bed':
                speak_message('Down')
                change_speak_message('Please move my bed down')
                self.curr_request_specification = 'Down 下'
            else:
                pass

        elif button == 'Middle':
            if location == 'English_Main':
                change_menu('English_Food')
                speak_message('Food selected')
                self.curr_request_type = 'Food 食品'
            elif location == 'English_Liquid':
                speak_message('Juice')
                change_speak_message('Please give me some juice')
                self.curr_request_specification = 'Juice 果汁'
            elif location == 'English_Toilet':
                speak_message('Poop')
                change_speak_message('I need to go poop')
                self.curr_request_specification = 'Poop o屎'
            elif location == 'English_Food':
                speak_message('Pork')
                change_speak_message('Please give me some pork')
                self.curr_request_specification = 'Pork 豬肉'
            elif location == 'English_Bed':
                speak_message('Up')
                change_speak_message('Please move my bed up')
                self.curr_request_specification = 'Up 上'
            else:
                pass

        elif button == 'Pinky':
            if location == 'English_Main':
                change_menu('English_Bed')
                speak_message('Bed selected')
                self.curr_request_type = 'Bed 床'
            elif location == 'English_Liquid':
                speak_message('Milk')
                change_speak_message('Please give me some milk')
                self.curr_request_specification = 'Milk 奶'
            elif location == 'English_Toilet':
                speak_message('Help')
                change_speak_message('Please help me go to the bathroom')
                self.curr_request_specification = 'Help 幫忙'
            elif location == 'English_Food':
                speak_message('Chicken')
                change_speak_message('Please give me some chicken')
                self.curr_request_specification = 'Chicken 雞肉'
            elif location == 'English_Bed':
                speak_message('Help')
                change_speak_message('I need help with my bed')
                self.curr_request_specification = 'Help 幫忙'
            else:
                pass

        elif button == 'Speak_Command':
            speak_message()
            change_speak_message('')
            new_request = Requests(request_type = self.curr_request_type, request_specification = self.curr_request_specification, request_patient = self.curr_request_patient)
            new_request.save()
            print(new_request)


        elif button == 'Cantonese':
            change_speak_message('')
            location = 'Cantonese'+location.replace('English','')
            screen_two = self.manager.get_screen('Cantonese_Window')
            screen_two.change_menu(location)

        sm.current = 'english'

class Cantonese_Window(Screen):
    def change_menu(self, menu):
        global location
        location = menu
        if location == 'Cantonese_Main':
            self.ids.Cantonese_Thumb_label.text = '飲品'
            self.ids.Cantonese_Index_label.text = '廁所'
            self.ids.Cantonese_Middle_label.text = '食物'
            self.ids.Cantonese_Pinky_label.text = '教床'
        elif location == 'Cantonese_Liquid':
            self.ids.Cantonese_Thumb_label.text = '離開'
            self.ids.Cantonese_Index_label.text = '水'
            self.ids.Cantonese_Middle_label.text = '果汁'
            self.ids.Cantonese_Pinky_label.text = '其他'
        elif location == 'Cantonese_Toilet':
            self.ids.Cantonese_Thumb_label.text = '離開選擇'
            self.ids.Cantonese_Index_label.text = '“o”尿'
            self.ids.Cantonese_Middle_label.text = '“o”屎'
            self.ids.Cantonese_Pinky_label.text = '其他'
        elif location == 'Cantonese_Food':
            self.ids.Cantonese_Thumb_label.text = '離開選擇'
            self.ids.Cantonese_Index_label.text = '食飯'
            self.ids.Cantonese_Middle_label.text = '豬肉'
            self.ids.Cantonese_Pinky_label.text = '其他'
        elif location == 'Cantonese_Bed':
            self.ids.Cantonese_Thumb_label.text = '離開選擇'
            self.ids.Cantonese_Index_label.text = '教低張床'
            self.ids.Cantonese_Middle_label.text = '教高張床'
            self.ids.Cantonese_Pinky_label.text = '其他'
        else:
            pass

    def button_press(self, button):
        def change_cantonese_message_name(file_name):
            global cantonese_message_name
            cantonese_message_name = file_name

        def speak_message(message='speak_command'):
            global cantonese_message_name
            if message == 'speak_command' and cantonese_message_name == '':
                pass
            elif message == 'speak_command':
                self.sound = SoundLoader.load(os.path.join('cantonese_audio',cantonese_message_name))
                self.sound.play()
                cantonese_message_name = ''
            else:
                self.sound = SoundLoader.load(os.path.join('cantonese_audio',message))
                self.sound.play()

        def change_menu(menu):
            global location
            location = menu
            if location == 'Cantonese_Main':
                self.ids.Cantonese_Thumb_label.text = '飲品'
                self.ids.Cantonese_Index_label.text = '廁所'
                self.ids.Cantonese_Middle_label.text = '食物'
                self.ids.Cantonese_Pinky_label.text = '教床'
            elif location == 'Cantonese_Liquid':
                self.ids.Cantonese_Thumb_label.text = '離開'
                self.ids.Cantonese_Index_label.text = '水'
                self.ids.Cantonese_Middle_label.text = '果汁'
                self.ids.Cantonese_Pinky_label.text = '其他'
            elif location == 'Cantonese_Toilet':
                self.ids.Cantonese_Thumb_label.text = '離開選擇'
                self.ids.Cantonese_Index_label.text = '“o”尿'
                self.ids.Cantonese_Middle_label.text = '“o”屎'
                self.ids.Cantonese_Pinky_label.text = '其他'
            elif location == 'Cantonese_Food':
                self.ids.Cantonese_Thumb_label.text = '離開選擇'
                self.ids.Cantonese_Index_label.text = '食飯'
                self.ids.Cantonese_Middle_label.text = '牛肉'
                self.ids.Cantonese_Pinky_label.text = '其他'
            elif location == 'Cantonese_Bed':
                self.ids.Cantonese_Thumb_label.text = '離開選擇'
                self.ids.Cantonese_Index_label.text = '教低張床'
                self.ids.Cantonese_Middle_label.text = '教高張床'
                self.ids.Cantonese_Pinky_label.text = '其他'
            else:
                pass

        global location
        if button == '拇指':
            if location == 'Cantonese_Main':
                change_menu('Cantonese_Liquid')
                speak_message('你選擇左飲品.mp3')
            elif location == 'Cantonese_Liquid':
                change_menu('Cantonese_Main')
                change_cantonese_message_name('')
                speak_message('離開選擇.mp3')
            elif location == 'Cantonese_Toilet':
                change_menu('Cantonese_Main')
                change_cantonese_message_name('')
                speak_message('離開選擇.mp3')
            elif location == 'Cantonese_Food':
                change_menu('Cantonese_Main')
                change_cantonese_message_name('')
                speak_message('離開選擇.mp3')
            elif location == 'Cantonese_Bed':
                change_menu('Cantonese_Main')
                change_cantonese_message_name('')
                speak_message('離開選擇.mp3')
            else:
                pass

        if button == '食指':
            if location == 'Cantonese_Main':
                change_menu('Cantonese_Toilet')
                speak_message('你選擇左廁所選項.mp3')
            elif location == 'Cantonese_Liquid':
                change_cantonese_message_name('我要飲水.mp3')
                speak_message('你選擇左​水.mp3')
            elif location == 'Cantonese_Toilet':
                change_cantonese_message_name('我要去“o”尿.mp3')
                speak_message('你選擇‘“o”尿選項.mp3')
            elif location == 'Cantonese_Food':
                change_cantonese_message_name('我想​食飯.mp3')
                speak_message('你選擇​食飯.mp3')
            elif location == 'Cantonese_Bed':
                change_cantonese_message_name('請幫我教低張床.mp3')
                speak_message('你選擇教​低​張床.mp3')
            else:
                pass

        if button == '中指':
            if location == 'Cantonese_Main':
                change_menu('Cantonese_Food')
                speak_message('你選擇左食物選項.mp3')
            elif location == 'Cantonese_Liquid':
                change_cantonese_message_name('我想要果汁.mp3')
                speak_message('你選擇左​果汁.mp3')
            elif location == 'Cantonese_Toilet':
                change_cantonese_message_name('我要去“o”屎.mp3')
                speak_message('你選擇‘“o”屎選項.mp3')
            elif location == 'Cantonese_Food':
                change_cantonese_message_name('我想食牛肉.mp3')
                speak_message('你選擇左牛肉.mp3')
            elif location == 'Cantonese_Bed':
                change_cantonese_message_name('請幫我教高張床.mp3')
                speak_message('你選擇教​高​張床.mp3')
            else:
                pass

        if button == '小指':
            if location == 'Cantonese_Main':
                change_menu('Cantonese_Bed')
                speak_message('你選擇左教床選項.mp3')
            elif location == 'Cantonese_Liquid':
                change_cantonese_message_name('你選擇左​其他.mp3')
                speak_message('你過來聽我.mp3')
            elif location == 'Cantonese_Toilet':
                change_cantonese_message_name('你選擇左​其他.mp3')
                speak_message('你過來聽我.mp3')
            elif location == 'Cantonese_Food':
                change_cantonese_message_name('你選擇左​其他.mp3')
                speak_message('你過來聽我.mp3')
            elif location == 'Cantonese_Bed':
                change_cantonese_message_name('你選擇左​其他.mp3')
                speak_message('你過來聽我.mp3')
            else:
                pass

        elif button == 'English':
            location = 'English'+location.replace('Cantonese','')
            screen_one = self.manager.get_screen('English_Window')
            screen_one.change_menu(location)

        if button == 'Speak_Command':
            speak_message()
            change_cantonese_message_name('')
        sm.current = 'canto'
# kv file
kv = Builder.load_file('login.kv')
sm = ScreenManager()
#smNT = ScreenManager(transition=NoTransition())

# reading all the data stored
users=pd.read_csv('login.csv')

# adding screens
sm.add_widget(loginWindow(name='login'))
sm.add_widget(signupWindow(name='signup'))
sm.add_widget(logDataWindow(name='logdata'))
sm.add_widget(English_Window(name='english'))
sm.add_widget(Cantonese_Window(name='canto'))

# class that builds gui
class loginMain(App):
    def build(self):
        return sm

# driver function
if __name__=="__main__":
    loginMain().run()
