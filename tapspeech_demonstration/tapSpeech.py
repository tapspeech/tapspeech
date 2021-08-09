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
LabelBase.register(name='Metropolis', fn_regular='Metropolis-Light.woff')

global_patient_name = ''
global_caretaker_name = ''

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

    def item_check(search, name):
        pat = Patient.objects.all().filter(patientFullName=name)
        if search == 'econ':
            if pat.values_list('patientEmergencyContact', flat=True).exists():
                econ1 = pat.values_list('patientEmergencyContact', flat=True)[0]
            else:
                econ1 = 'Contact Name / Contact Number'
            if pat.values_list('patientEmergencyContact2', flat=True).exists():
                econ2 = pat.values_list('patientEmergencyContact2', flat=True)[0]
            else:
                econ2 = 'Contact Name / Contact Number'
            if pat.values_list('patientEmergencyContact3', flat=True).exists():
                econ3 = pat.values_list('patientEmergencyContact3', flat=True)[0]
            else:
                econ3 = 'Contact Name / Contact Number'
            econlist = [econ1, econ2, econ3]
            return econlist
        if search == 'medhis':
            if pat.values_list('patientMedicalHistory', flat=True).exists():
                medhis1 = pat.values_list('patientMedicalHistory', flat=True)[0]
            else:
                medhis1 = 'Medical History'
            if pat.values_list('patientDiagnosis', flat=True).exists():
                medhis2 = pat.values_list('patientDiagnosis', flat=True)[0]
            else:
                medhis2 = 'Patient Diagnosis'
            if pat.values_list('patientMedication', flat=True).exists():
                medhis3 = pat.values_list('patientMedication', flat=True)[0]
            else:
                medhis3 = 'Patient Medication'
            medhislist = [medhis1, medhis2, medhis3]
            return medhislist

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

    #get patient medical history, diagnosis and medication info
    def get_patient_info(name, type):
        patient_no = none
        #selects the database
        test = ReadSQL('db.sqlite3')
        df = test.query_columns_to_dataframe('tapSpeech_app_patient', ['patientMedicalHistory'])
        df2 = test.query_columns_to_dataframe('tapSpeech_app_patient', ['patientDiagnosis'])
        df3 = test.query_columns_to_dataframe('tapSpeech_app_patient', ['patientMedication'])
        df4 = test.query_columns_to_dataframe('tapSpeech_app_patient', ['patientFullName'])
        #adds all names and birthday into the emails list
        for number in range(len(df.index)):
            if name == df4.at[number,'patientFullName']:
                patient_no = number
        if type == 1:
            return df.at[patient_no,'patientMedicalHistory']
        if type == 2:
            return df2.at[patient_no,'patientDiagnosis']
        if type == 3:
            return df3.at[patient_no,'patientMedication']

    def new_request_puller(name):
        names = name
        names_len = len(names)
        timer = 0
        reqlist = []
        for i in range(names_len):
            success = False
            print(timer)
            reqs = Requests.objects.all().filter(request_patient=names[timer])
            context = reqs.distinct().order_by('-request_date', '-request_time')
            if context.values_list('request_patient', flat=True).exists():
                r_pat = context.values_list('request_patient', flat=True)[0]
                r_type = context.values_list('request_type', flat=True)[0]
                r_spec = context.values_list('request_specification', flat=True)[0]
                r_time = context.values_list('request_time', flat=True)[0]
                success = True
            else:
                success = False

            if timer == 0:
                if success == True:
                    req0 = [r_pat, r_type, r_spec, r_time]
                if success == False:
                    req0 = ['None', 'None', 'None', 'None']
                reqlist.append(req0)
            if timer == 1:
                if success == True:
                    req1 = [r_pat, r_type, r_spec, r_time]
                if success == False:
                    req1 = ['None', 'None', 'None', 'None']
                reqlist.append(req1)
            if timer == 2:
                if success == True:
                    req2 = [r_pat, r_type, r_spec, r_time]
                if success == False:
                    req2 = ['None', 'None', 'None', 'None']
                reqlist.append(req2)
            if timer == 3:
                if success == True:
                    req3 = [r_pat, r_type, r_spec, r_time]
                if success == False:
                    req3 = ['None', 'None', 'None', 'None']
                reqlist.append(req3)
            if timer == 4:
                if success == True:
                    req4 = [r_pat, r_type, r_spec, r_time]
                if success == False:
                    req4 = ['None', 'None', 'None', 'None']
                reqlist.append(req4)
            if timer == 5:
                if success == True:
                    req5 = [r_pat, r_type, r_spec, r_time]
                if success == False:
                    req5 = ['None', 'None', 'None', 'None']
                reqlist.append(req5)
            timer += 1
        return reqlist


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

        tz_HK = pytz.timezone('Hongkong')
        datetime_HK = datetime.now(tz_HK)
        current_day = datetime_HK.strftime("%d/%m/%Y")
        current_time = datetime_HK.strftime("%H:%M:%S")
        print(current_day)
        print(message + " " + self.request_type)
        new_request = Requests(request_type = self.request_type, request_specification = message, request_patient = global_patient_name, request_time = current_time, request_date = current_day)
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
    emergency_contact_1 = ObjectProperty(None)
    emergency_contact_2 = ObjectProperty(None)
    emergency_contact_3 = ObjectProperty(None)

    # Change below to use database values
    def update_emergency_contacts(self):
        global global_patient_name
        econlist = ReadSQL.item_check('econ', global_patient_name)
        self.emergency_contact_1.text = econlist[0]
        self.emergency_contact_2.text = econlist[1]
        self.emergency_contact_3.text = econlist[2]

    # Save the new_emergency_contact_x_value into the database
    def save_Contacts(self):
        global global_patient_name
        Patient.objects.filter(patientFullName=global_patient_name).update(patientEmergencyContact=self.emergency_contact_1.text)
        Patient.objects.filter(patientFullName=global_patient_name).update(patientEmergencyContact2=self.emergency_contact_2.text)
        Patient.objects.filter(patientFullName=global_patient_name).update(patientEmergencyContact3=self.emergency_contact_3.text)

class en_informationScreen(Screen):
    medical_history_input = ObjectProperty(None)
    diagnosis_input = ObjectProperty(None)
    medication_input = ObjectProperty(None)

    # Change below to use database values
    def update_medical_info(self):
        global global_patient_name
        medhislist = ReadSQL.item_check('medhis', global_patient_name)
        self.medical_history_input.text = medhislist[0]
        self.diagnosis_input.text = medhislist[1]
        self.medication_input.text = medhislist[2]

    # Save the new medical_info into the database
    def save_medical_info(self):
        global global_patient_name
        Patient.objects.filter(patientFullName=global_patient_name).update(patientMedicalHistory=self.medical_history_input.text)
        Patient.objects.filter(patientFullName=global_patient_name).update(patientDiagnosis=self.diagnosis_input.text)
        Patient.objects.filter(patientFullName=global_patient_name).update(patientMedication=self.medication_input.text)

class en_caretakerUpScreen(Screen):
    caretaker_name = ObjectProperty(None)

    label_1_bg = ObjectProperty(None)
    label_2_bg = ObjectProperty(None)
    label_3_bg = ObjectProperty(None)
    label_4_bg = ObjectProperty(None)
    label_5_bg = ObjectProperty(None)
    label_6_bg = ObjectProperty(None)

    patient_1_request = ObjectProperty(None)
    patient_2_request = ObjectProperty(None)
    patient_3_request = ObjectProperty(None)
    patient_4_request = ObjectProperty(None)
    patient_5_request = ObjectProperty(None)
    patient_6_request = ObjectProperty(None)

    clear_button_1 = ObjectProperty(None)
    clear_button_2 = ObjectProperty(None)
    clear_button_3 = ObjectProperty(None)
    clear_button_4 = ObjectProperty(None)
    clear_button_5 = ObjectProperty(None)
    clear_button_6 = ObjectProperty(None)

    def display_caretaker_name(self):
        global global_caretaker_name
        self.caretaker_name.text = 'Caretaker: '+global_caretaker_name

    def update_requests(self):
        pass

    def build_patient_list():
        caretakers_patient_list = []
        ct = Caretaker.objects.all().filter(caretakerFullName = global_caretaker_name)
        if ct.values_list('listedPatients', flat=True).exists():
            lpat = ct.values_list('listedPatients', flat=True)[0]
            caretakers_patient_list.append(lpat)
        if ct.values_list('listedPatients2', flat=True).exists():
            lpat2 = ct.values_list('listedPatients2', flat=True)[0]
            caretakers_patient_list.append(lpat2)
        if ct.values_list('listedPatients3', flat=True).exists():
            lpat3 = ct.values_list('listedPatients3', flat=True)[0]
            caretakers_patient_list.append(lpat3)
        if ct.values_list('listedPatients4', flat=True).exists():
            lpat4 = ct.values_list('listedPatients4', flat=True)[0]
            caretakers_patient_list.append(lpat4)
        if ct.values_list('listedPatients5', flat=True).exists():
            lpat5 = ct.values_list('listedPatients5', flat=True)[0]
            caretakers_patient_list.append(lpat5)
        return caretakers_patient_list

    def new_request_pull(self):
        caretakers_patient_list = en_caretakerUpScreen.build_patient_list()
        reqlist = ReadSQL.new_request_puller(caretakers_patient_list) # 'LIST' SHOULD EVENTUALLY BE REPLACED WITH THE CARETAKER'S ACTUAL PATIENT LIST
        return(reqlist)

    def refresh(self):
        reqlist = self.new_request_pull()

        # Checks if there are no requests and deltes them
        new_reqlist = []
        processed_range = 0
        while processed_range < len(reqlist):
            if reqlist[processed_range][0] == 'None' and reqlist[processed_range][1] == 'None' and reqlist[processed_range][2] == 'None' and reqlist[processed_range][3] == 'None':
                pass
            else:
                new_reqlist.append(reqlist[processed_range])
            processed_range = processed_range + 1
        reqlist = new_reqlist

        number_of_requests = len(reqlist)
        print(reqlist)

        processed_request = 0
        # Sets default for all labels to be visible
        while processed_request < 6:
            if processed_request == 0:
                self.label_6_bg.size_hint = (0.861, 0.0737)
                self.patient_6_request.size_hint = (0.663, 0.0737)
                self.patient_6_request.text = ''
                self.clear_button_6.size_hint = (0.0742, 0.0350)
            elif processed_request == 1:
                self.label_5_bg.size_hint = (0.861, 0.0737)
                self.patient_5_request.size_hint = (0.663, 0.0737)
                self.patient_5_request.text = ''
                self.clear_button_5.size_hint = (0.0742, 0.0350)
            elif processed_request == 2:
                self.label_4_bg.size_hint = (0.861, 0.0737)
                self.patient_4_request.size_hint = (0.663, 0.0737)
                self.patient_4_request.text = ''
                self.clear_button_4.size_hint = (0.0742, 0.0350)
            elif processed_request == 3:
                self.label_3_bg.size_hint = (0.861, 0.0737)
                self.patient_3_request.size_hint = (0.663, 0.0737)
                self.patient_3_request.text = ''
                self.clear_button_3.size_hint = (0.0742, 0.0350)
            elif processed_request == 4:
                self.label_2_bg.size_hint = (0.861, 0.0737)
                self.patient_2_request.size_hint = (0.663, 0.0737)
                self.patient_2_request.text = ''
                self.clear_button_2.size_hint = (0.0742, 0.0350)
            elif processed_request == 5:
                self.label_1_bg.size_hint = (0.861, 0.0737)
                self.patient_1_request.size_hint = (0.663, 0.0737)
                self.patient_1_request.text = ''
                self.clear_button_1.size_hint = (0.0742, 0.0350)
            processed_request = processed_request + 1

        processed_request = 0
        # Deletes all empty request slots
        while processed_request < 6-number_of_requests:
            if processed_request == 0:
                self.label_6_bg.size_hint = (0.861, 0)
                self.patient_6_request.size_hint = (0.861, 0)
                self.patient_6_request.text = ''
                self.clear_button_6.size_hint = (0.861, 0)
            elif processed_request == 1:
                self.label_5_bg.size_hint = (0.861, 0)
                self.patient_5_request.size_hint = (0.861, 0)
                self.patient_5_request.text = ''
                self.clear_button_5.size_hint = (0.861, 0)
            elif processed_request == 2:
                self.label_4_bg.size_hint = (0.861, 0)
                self.patient_4_request.size_hint = (0.861, 0)
                self.patient_4_request.text = ''
                self.clear_button_4.size_hint = (0.861, 0)
            elif processed_request == 3:
                self.label_3_bg.size_hint = (0.861, 0)
                self.patient_3_request.size_hint = (0.861, 0)
                self.patient_3_request.text = ''
                self.clear_button_3.size_hint = (0.861, 0)
            elif processed_request == 4:
                self.label_2_bg.size_hint = (0.861, 0)
                self.patient_2_request.size_hint = (0.861, 0)
                self.patient_2_request.text = ''
                self.clear_button_2.size_hint = (0.861, 0)
            elif processed_request == 5:
                self.label_1_bg.size_hint = (0.861, 0)
                self.patient_1_request.size_hint = (0.861, 0)
                self.patient_1_request.text = ''
                self.clear_button_1.size_hint = (0.861, 0)
            else:
                pass
            processed_request = processed_request + 1

        processed_request = 0
        # Fills the proper requests into the UI:
        while processed_request < number_of_requests:
            request = reqlist[processed_request]
            print(request)
            request = request[3] + ' | ' + request[0] + ' | ' + request[1] + ': ' + request[2]
            if processed_request == 0:
                self.patient_1_request.text = request
            elif processed_request == 1:
                self.patient_2_request.text = request
            elif processed_request == 2:
                self.patient_3_request.text = request
            elif processed_request == 3:
                self.patient_4_request.text = request
            elif processed_request == 4:
                self.patient_5_request.text = request
            elif processed_request == 5:
                self.patient_6_request.text = request
            processed_request = processed_request + 1

        '''
        below is only for demonstration purposes
        '''
        self.label_1_bg.size_hint = (0.861, 0.0737)
        self.patient_1_request.size_hint = (0.663, 0.0737)
        self.patient_1_request.text = 'Gabriel: Please give some water'
        self.clear_button_1.size_hint = (0.0742, 0.0350)

    def delete_request(self,label_number):
        self.label_1_bg.size_hint = (0.861, 0)
        self.patient_1_request.size_hint = (0.861, 0)
        self.patient_1_request.text = ''
        self.clear_button_1.size_hint = (0.861, 0)

        # if label_number == 1:
        #     message = self.patient_1_request.text
        # elif label_number == 2:
        #     message = self.patient_2_request.text
        # elif label_number == 3:
        #     message = self.patient_3_request.text
        # elif label_number == 4:
        #     message = self.patient_4_request.text
        # elif label_number == 5:
        #     message = self.patient_5_request.text
        # elif label_number == 6:
        #     message = self.patient_6_request.text
        #
        # message = message.split(' | ')
        # message_specification_split = message[2].split(': ')
        # reformatted_message = []
        # reformatted_message.append(message[1]) # NAME
        # reformatted_message.append(message_specification_split[0]) # TYPE
        # reformatted_message.append(message_specification_split[1]) # SPEC
        # reformatted_message.append(message[0]) # TIME
        #
        # print(reformatted_message[3])
        #
        # Requests.objects.filter(request_patient=reformatted_message[0], request_type=reformatted_message[1], request_specification=reformatted_message[2], request_time=reformatted_message[3]).delete()
        #
        # self.refresh()

class en_caretakerDownScreen(Screen):
    top_left_image = ObjectProperty(None)
    top_right_image = ObjectProperty(None)
    mid_left_image = ObjectProperty(None)
    mid_right_image = ObjectProperty(None)
    bottom_left_image = ObjectProperty(None)
    bottom_right_image = ObjectProperty(None)

    top_left_label = ObjectProperty(None)
    top_right_image = ObjectProperty(None)
    mid_left_image = ObjectProperty(None)
    mid_right_image = ObjectProperty(None)
    bottom_left_image = ObjectProperty(None)
    bottom_right_image = ObjectProperty(None)

    ''


    def update_screen(self):
        pass


class en_updatepatientlistScreen(Screen):
    patient_username = ObjectProperty(None)
    patient_password = ObjectProperty(None)

    def validate(name, password):
        passwordcorrect = False
        pat = Patient.objects.all().filter(patientFullName=name)
        if pat.values_list('patientBirthDate', flat=True).exists():
            corrpassword = pat.values_list('patientBirthDate', flat=True)[0]
            if password == corrpassword:
                passwordcorrect = True
            return passwordcorrect
        else:
            passwordcorrect = False


    def checkslots(ctname):
        emptyslots = [1, 2, 3, 4, 5, 6]
        ct = Caretaker.objects.all().filter(caretakerFullName = global_caretaker_name)
        if ct.values_list('listedPatients', flat=True).exists():
            es1 = ct.values_list('listedPatients', flat=True)[0]
            if es1 != "":
                emptyslots.remove(1)
        if ct.values_list('listedPatients2', flat=True).exists():
            es2 = ct.values_list('listedPatients2', flat=True)[0]
            if es2 != "":
                emptyslots.remove(2)
        if ct.values_list('listedPatients3', flat=True).exists():
            es3 = ct.values_list('listedPatients3', flat=True)[0]
            if es3 != "":
                emptyslots.remove(3)
        if ct.values_list('listedPatients4', flat=True).exists():
            es4 = ct.values_list('listedPatients4', flat=True)[0]
            if es4 != "":
                emptyslots.remove(4)
        if ct.values_list('listedPatients5', flat=True).exists():
            es5 = ct.values_list('listedPatients5', flat=True)[0]
            if es5 != "":
                emptyslots.remove(5)
        if ct.values_list('listedPatients6', flat=True).exists():
            es6 = ct.values_list('listedPatients6', flat=True)[0]
            if es6 != "":
                emptyslots.remove(6)
        return emptyslots

    def checkfilledslots(ctname):
        filledslots = [ ]
        ct = Caretaker.objects.all().filter(caretakerFullName = global_caretaker_name)
        if ct.values_list('listedPatients', flat=True).exists():
            es1 = ct.values_list('listedPatients', flat=True)[0]
            if es1 != "":
                filledslots.append(1)
        if ct.values_list('listedPatients2', flat=True).exists():
            es2 = ct.values_list('listedPatients2', flat=True)[0]
            if es2 != "":
                filledslots.append(2)
        if ct.values_list('listedPatients3', flat=True).exists():
            es3 = ct.values_list('listedPatients3', flat=True)[0]
            if es3 != "":
                filledslots.append(3)
        if ct.values_list('listedPatients4', flat=True).exists():
            es4 = ct.values_list('listedPatients4', flat=True)[0]
            if es4 != "":
                filledslots.append(4)
        if ct.values_list('listedPatients5', flat=True).exists():
            es5 = ct.values_list('listedPatients5', flat=True)[0]
            if es5 != "":
                filledslots.append(5)
        if ct.values_list('listedPatients6', flat=True).exists():
            es6 = ct.values_list('listedPatients6', flat=True)[0]
            if es6 != "":
                filledslots.append(6)
        return filledslots

    def checkforcopies(ctname, ptname):
        nocopies = True
        ct = Caretaker.objects.all().filter(caretakerFullName = global_caretaker_name)
        if ct.values_list('listedPatients', flat=True).exists():
            es1 = ct.values_list('listedPatients', flat=True)[0]
            if es1 == ptname:
                nocopies = False
        if ct.values_list('listedPatients2', flat=True).exists():
            es2 = ct.values_list('listedPatients2', flat=True)[0]
            if es2 == ptname:
                nocopies = False
        if ct.values_list('listedPatients3', flat=True).exists():
            es3 = ct.values_list('listedPatients3', flat=True)[0]
            if es3 == ptname:
                nocopies = False
        if ct.values_list('listedPatients4', flat=True).exists():
            es4 = ct.values_list('listedPatients4', flat=True)[0]
            if es4 == ptname:
                nocopies = False
        if ct.values_list('listedPatients5', flat=True).exists():
            es5 = ct.values_list('listedPatients5', flat=True)[0]
            if es5 == ptname:
                nocopies = False
        if ct.values_list('listedPatients6', flat=True).exists():
            es6 = ct.values_list('listedPatients6', flat=True)[0]
            if es6 == ptname:
                nocopies = False
        return nocopies

    def addorremove_patient(self, addorremove):
        username_value = self.patient_username.text
        password_value = self.patient_password.text
        self.patient_username.text = ''
        self.patient_password.text = ''

        '''
        also make an if else statement that checks if the caretaker has 6 patients already (maximum)
        '''
        global global_caretaker_name
        ct = Caretaker.objects.all().filter(caretakerFullName = global_caretaker_name)

        if addorremove == 'add':
            if en_updatepatientlistScreen.checkforcopies(global_caretaker_name, username_value):
                    if en_updatepatientlistScreen.validate(username_value, password_value) == True:
                        avalibleslots = en_updatepatientlistScreen.checkslots(global_caretaker_name)
                        print(avalibleslots)
                        avalibleslots_len = len(avalibleslots)
                        if avalibleslots_len == 0:
                            error(1) # IF THERE ARE NO AVALIBLE SLOTS
                        else:
                            if avalibleslots[0] == 1:
                                Caretaker.objects.filter(caretakerFullName=global_caretaker_name).update(listedPatients=username_value)
                            if avalibleslots[0] == 2:
                                Caretaker.objects.filter(caretakerFullName=global_caretaker_name).update(listedPatients2=username_value)
                            if avalibleslots[0] == 3:
                                Caretaker.objects.filter(caretakerFullName=global_caretaker_name).update(listedPatients3=username_value)
                            if avalibleslots[0] == 4:
                                Caretaker.objects.filter(caretakerFullName=global_caretaker_name).update(listedPatients4=username_value)
                            if avalibleslots[0] == 5:
                                Caretaker.objects.filter(caretakerFullName=global_caretaker_name).update(listedPatients5=username_value)
                            if avalibleslots[0] == 6:
                                Caretaker.objects.filter(caretakerFullName=global_caretaker_name).update(listedPatients6=username_value)
                    else:
                        error(1) # IF NAME IS ALREADY LISTED
            else:
                error(1) # IF THE USERNAME AND PASSWORD DOESN'T EXIST / DOESN'T MATCH


        elif addorremove == 'remove':
            if en_updatepatientlistScreen.validate(username_value, password_value) == True:
                filledslots = en_updatepatientlistScreen.checkfilledslots(global_caretaker_name)
                usedslots_len = len(filledslots)
                if usedslots_len == 0:
                    error(1) # IF THERE ARE NO AVALIBLE SLOTS
                else:
                    if ct.values_list('listedPatients', flat=True).exists():
                        lpat = ct.values_list('listedPatients', flat=True)[0]
                        if lpat == username_value:
                            Caretaker.objects.filter(caretakerFullName=global_caretaker_name).update(listedPatients='')
                    if ct.values_list('listedPatients2', flat=True).exists():
                        lpat = ct.values_list('listedPatients2', flat=True)[0]
                        if lpat == username_value:
                            Caretaker.objects.filter(caretakerFullName=global_caretaker_name).update(listedPatients2='')
                    if ct.values_list('listedPatients3', flat=True).exists():
                        lpat = ct.values_list('listedPatients3', flat=True)[0]
                        if lpat == username_value:
                            Caretaker.objects.filter(caretakerFullName=global_caretaker_name).update(listedPatients3='')
                    if ct.values_list('listedPatients4', flat=True).exists():
                        lpat = ct.values_list('listedPatients4', flat=True)[0]
                        if lpat == username_value:
                            Caretaker.objects.filter(caretakerFullName=global_caretaker_name).update(listedPatients4='')
                    if ct.values_list('listedPatients5', flat=True).exists():
                        lpat = ct.values_list('listedPatients5', flat=True)[0]
                        if lpat == username_value:
                            Caretaker.objects.filter(caretakerFullName=global_caretaker_name).update(listedPatients5='')
                    self.patient_username.text = ''
                    self.patient_password.text = ''
            else:
                error(1)


class ct_welcomeScreen(Screen):
    pass

class ct_loginScreen(Screen):
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
                print(completed_login)
                if completed_login == 'patient':
                    App.get_running_app().sm.current = 'ct_patientUp'
                    global global_patient_name
                    global_patient_name = self.username.text
                    #elif completed_login == 'caretaker' or completed_login == 'None' or completed_login == ''
                    #fix this for some reason completed_login is 'None'
                else:
                    print('senses is caretaker')
                    App.get_running_app().sm.current = 'ct_caretakerUp'

                    '''
                    I dont know what the two lines,
                    remove this comment if those lines are necessary
                    '''

                    global global_caretaker_name
                    global_caretaker_name = self.username.text

class ct_registerScreen(Screen):
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
                    App.get_running_app().sm.current = 'ct_patientUp'
                    global global_patient_name
                    global_patient_name = self.username.text
                elif user_type == 'caretaker':
                    print('running')
                    App.get_running_app().sm.current = 'ct_caretakerUp'

                    '''
                    I dont know what the two lines,
                    remove this comment if those lines are necessary
                    '''

                    global global_caretaker_name
                    global_caretaker_name = self.username.text
                else:
                    print('running error')
                    error(3)

class ct_patientUpScreen(Screen):
    say_something = ObjectProperty(None)
    hello_name = ObjectProperty(None)

    def sound_alarm(self):
        self.sound = SoundLoader.load(os.path.join('audio','ios_ringtone.mp3'))
        self.sound.play()

    def change_helloMessage(self):
        global global_patient_name
        self.hello_name.text = '你好,' + global_patient_name

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

        tz_HK = pytz.timezone('Hongkong')
        datetime_HK = datetime.now(tz_HK)
        current_day = datetime_HK.strftime("%d/%m/%Y")
        current_time = datetime_HK.strftime("%H:%M:%S")
        print(current_day)
        print(message + " " + self.request_type)
        new_request = Requests(request_type = self.request_type, request_specification = message, request_patient = global_patient_name, request_time = current_time, request_date = current_day)
        new_request.save()
        print(new_request)

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

class ct_contactsScreen(Screen):
    emergency_contact_1 = ObjectProperty(None)
    emergency_contact_2 = ObjectProperty(None)
    emergency_contact_3 = ObjectProperty(None)

    # Change below to use database values
    def update_emergency_contacts(self):
        global global_patient_name
        econlist = ReadSQL.item_check('econ', global_patient_name)
        self.emergency_contact_1.text = econlist[0]
        self.emergency_contact_2.text = econlist[1]
        self.emergency_contact_3.text = econlist[2]

    def save_Contacts(self):
        global global_patient_name
        Patient.objects.filter(patientFullName=global_patient_name).update(patientEmergencyContact=self.emergency_contact_1.text)
        Patient.objects.filter(patientFullName=global_patient_name).update(patientEmergencyContact2=self.emergency_contact_2.text)
        Patient.objects.filter(patientFullName=global_patient_name).update(patientEmergencyContact3=self.emergency_contact_3.text)

class ct_informationScreen(Screen):
    medical_history_input = ObjectProperty(None)
    diagnosis_input = ObjectProperty(None)
    medication_input = ObjectProperty(None)

    # Change below to use database values
    def update_medical_info(self):
        global global_patient_name
        medhislist = ReadSQL.item_check('medhis', global_patient_name)
        self.medical_history_input.text = medhislist[0]
        self.diagnosis_input.text = medhislist[1]
        self.medication_input.text = medhislist[2]

    # Save the new medical_info into the database
    def save_medical_info(self):
        global global_patient_name
        Patient.objects.filter(patientFullName=global_patient_name).update(patientMedicalHistory=self.medical_history_input.text)
        Patient.objects.filter(patientFullName=global_patient_name).update(patientDiagnosis=self.diagnosis_input.text)
        Patient.objects.filter(patientFullName=global_patient_name).update(patientMedication=self.medication_input.text)


class ct_caretakerUpScreen(Screen):
    caretaker_name = ObjectProperty(None)

    Label_1_bg = ObjectProperty(None)
    Label_2_bg = ObjectProperty(None)
    Label_3_bg = ObjectProperty(None)
    Label_4_bg = ObjectProperty(None)
    Label_5_bg = ObjectProperty(None)
    Label_6_bg = ObjectProperty(None)

    patient_1_request = ObjectProperty(None)
    patient_2_request = ObjectProperty(None)
    patient_3_request = ObjectProperty(None)
    patient_4_request = ObjectProperty(None)
    patient_5_request = ObjectProperty(None)
    patient_6_request = ObjectProperty(None)

    clear_button_1 = ObjectProperty(None)
    clear_button_2 = ObjectProperty(None)
    clear_button_3 = ObjectProperty(None)
    clear_button_4 = ObjectProperty(None)
    clear_button_5 = ObjectProperty(None)
    clear_button_6 = ObjectProperty(None)

    def display_caretaker_name(self):
        global global_caretaker_name
        self.caretaker_name.text = '看護人：'+global_caretaker_name

    def update_requests(self):
        pass

    def build_patient_list():
        caretakers_patient_list = []
        ct = Caretaker.objects.all().filter(caretakerFullName = global_caretaker_name)
        if ct.values_list('listedPatients', flat=True).exists():
            lpat = ct.values_list('listedPatients', flat=True)[0]
            caretakers_patient_list.append(lpat)
        if ct.values_list('listedPatients2', flat=True).exists():
            lpat2 = ct.values_list('listedPatients2', flat=True)[0]
            caretakers_patient_list.append(lpat2)
        if ct.values_list('listedPatients3', flat=True).exists():
            lpat3 = ct.values_list('listedPatients3', flat=True)[0]
            caretakers_patient_list.append(lpat3)
        if ct.values_list('listedPatients4', flat=True).exists():
            lpat4 = ct.values_list('listedPatients4', flat=True)[0]
            caretakers_patient_list.append(lpat4)
        if ct.values_list('listedPatients5', flat=True).exists():
            lpat5 = ct.values_list('listedPatients5', flat=True)[0]
            caretakers_patient_list.append(lpat5)
        return caretakers_patient_list

    def new_request_pull(self):
        caretakers_patient_list = en_caretakerUpScreen.build_patient_list()
        reqlist = ReadSQL.new_request_puller(caretakers_patient_list) # 'LIST' SHOULD EVENTUALLY BE REPLACED WITH THE CARETAKER'S ACTUAL PATIENT LIST
        return(reqlist)

    def refresh(self):
        reqlist = self.new_request_pull()

        # Checks if there are no requests and deltes them
        new_reqlist = []
        processed_range = 0
        while processed_range < len(reqlist):
            if reqlist[processed_range][0] == 'None' and reqlist[processed_range][1] == 'None' and reqlist[processed_range][2] == 'None' and reqlist[processed_range][3] == 'None':
                pass
            else:
                new_reqlist.append(reqlist[processed_range])
            processed_range = processed_range + 1
        reqlist = new_reqlist

        number_of_requests = len(reqlist)
        print(reqlist)

        processed_request = 0
        # Sets default for all labels to be visible
        while processed_request < 6:
            if processed_request == 0:
                self.label_6_bg.size_hint = (0.861, 0.0737)
                self.patient_6_request.size_hint = (0.663, 0.0737)
                self.patient_6_request.text = ''
                self.clear_button_6.size_hint = (0.0742, 0.0350)
            elif processed_request == 1:
                self.label_5_bg.size_hint = (0.861, 0.0737)
                self.patient_5_request.size_hint = (0.663, 0.0737)
                self.patient_5_request.text = ''
                self.clear_button_5.size_hint = (0.0742, 0.0350)
            elif processed_request == 2:
                self.label_4_bg.size_hint = (0.861, 0.0737)
                self.patient_4_request.size_hint = (0.663, 0.0737)
                self.patient_4_request.text = ''
                self.clear_button_4.size_hint = (0.0742, 0.0350)
            elif processed_request == 3:
                self.label_3_bg.size_hint = (0.861, 0.0737)
                self.patient_3_request.size_hint = (0.663, 0.0737)
                self.patient_3_request.text = ''
                self.clear_button_3.size_hint = (0.0742, 0.0350)
            elif processed_request == 4:
                self.label_2_bg.size_hint = (0.861, 0.0737)
                self.patient_2_request.size_hint = (0.663, 0.0737)
                self.patient_2_request.text = ''
                self.clear_button_2.size_hint = (0.0742, 0.0350)
            elif processed_request == 5:
                self.label_1_bg.size_hint = (0.861, 0.0737)
                self.patient_1_request.size_hint = (0.663, 0.0737)
                self.patient_1_request.text = ''
                self.clear_button_1.size_hint = (0.0742, 0.0350)
            processed_request = processed_request + 1

        processed_request = 0
        # Deletes all empty request slots
        while processed_request < 6-number_of_requests:
            if processed_request == 0:
                self.label_6_bg.size_hint = (0.861, 0)
                self.patient_6_request.size_hint = (0.861, 0)
                self.patient_6_request.text = ''
                self.clear_button_6.size_hint = (0.861, 0)
            elif processed_request == 1:
                self.label_5_bg.size_hint = (0.861, 0)
                self.patient_5_request.size_hint = (0.861, 0)
                self.patient_5_request.text = ''
                self.clear_button_5.size_hint = (0.861, 0)
            elif processed_request == 2:
                self.label_4_bg.size_hint = (0.861, 0)
                self.patient_4_request.size_hint = (0.861, 0)
                self.patient_4_request.text = ''
                self.clear_button_4.size_hint = (0.861, 0)
            elif processed_request == 3:
                self.label_3_bg.size_hint = (0.861, 0)
                self.patient_3_request.size_hint = (0.861, 0)
                self.patient_3_request.text = ''
                self.clear_button_3.size_hint = (0.861, 0)
            elif processed_request == 4:
                self.label_2_bg.size_hint = (0.861, 0)
                self.patient_2_request.size_hint = (0.861, 0)
                self.patient_2_request.text = ''
                self.clear_button_2.size_hint = (0.861, 0)
            elif processed_request == 5:
                self.label_1_bg.size_hint = (0.861, 0)
                self.patient_1_request.size_hint = (0.861, 0)
                self.patient_1_request.text = ''
                self.clear_button_1.size_hint = (0.861, 0)
            else:
                pass
            processed_request = processed_request + 1

        processed_request = 0
        # Fills the proper requests into the UI:
        while processed_request < number_of_requests:
            request = reqlist[processed_request]
            print(request)
            request = request[3] + ' | ' + request[0] + ' | ' + request[1] + ': ' + request[2]
            if processed_request == 0:
                self.patient_1_request.text = request
            elif processed_request == 1:
                self.patient_2_request.text = request
            elif processed_request == 2:
                self.patient_3_request.text = request
            elif processed_request == 3:
                self.patient_4_request.text = request
            elif processed_request == 4:
                self.patient_5_request.text = request
            elif processed_request == 5:
                self.patient_6_request.text = request
            processed_request = processed_request + 1

    def delete_request(self,label_number):
        if label_number == 1:
            message = self.patient_1_request.text
        elif label_number == 2:
            message = self.patient_2_request.text
        elif label_number == 3:
            message = self.patient_3_request.text
        elif label_number == 4:
            message = self.patient_4_request.text
        elif label_number == 5:
            message = self.patient_5_request.text
        elif label_number == 6:
            message = self.patient_6_request.text

        message = message.split(' | ')
        message_specification_split = message[2].split(': ')
        reformatted_message = []
        reformatted_message.append(message[1]) # NAME
        reformatted_message.append(message_specification_split[0]) # TYPE
        reformatted_message.append(message_specification_split[1]) # SPEC
        reformatted_message.append(message[0]) # TIME

        print(reformatted_message[3])

        Requests.objects.filter(request_patient=reformatted_message[0], request_type=reformatted_message[1], request_specification=reformatted_message[2], request_time=reformatted_message[3]).delete()

        self.refresh()


class ct_caretakerDownScreen(Screen):
    top_left_image = ObjectProperty(None)
    top_right_image = ObjectProperty(None)
    mid_left_image = ObjectProperty(None)
    mid_right_image = ObjectProperty(None)
    bottom_left_image = ObjectProperty(None)
    bottom_right_image = ObjectProperty(None)

    top_left_label = ObjectProperty(None)
    top_right_image = ObjectProperty(None)
    mid_left_image = ObjectProperty(None)
    mid_right_image = ObjectProperty(None)
    bottom_left_image = ObjectProperty(None)
    bottom_right_image = ObjectProperty(None)

    def update_screen(self):
        pass

class ct_updatepatientlistScreen(Screen):
    patient_username = ObjectProperty(None)
    patient_password = ObjectProperty(None)
    #validates if password is correct for a username
    def validate(name, password):
        passwordcorrect = False
        pat = Patient.objects.all().filter(patientFullName=name)
        corrpassword = pat.values_list('patientBirthDate', flat=True)[0]
        if password == corrpassword:
            passwordcorrect = True
        return passwordcorrect

    def checkslots(ctname):
        emptyslots = [1, 2, 3, 4, 5, 6]
        if ct.values_list('listedPatients', flat=True).exists():
            emptyslots.remove(1)
        if ct.values_list('listedPatients2', flat=True).exists():
            emptyslots.remove(2)
        if ct.values_list('listedPatients3', flat=True).exists():
            emptyslots.remove(3)
        if ct.values_list('listedPatients4', flat=True).exists():
            emptyslots.remove(4)
        if ct.values_list('listedPatients5', flat=True).exists():
            emptyslots.remove(5)
        if ct.values_list('listedPatients6', flat=True).exists():
            emptyslots.remove(6)
        return emptyslots

    def checkfilledslots(ctname):
        filledslots = [ ]
        if ct.values_list('listedPatients', flat=True).exists():
            filledslots.remove(1)
        if ct.values_list('listedPatients2', flat=True).exists():
            filledslots.remove(2)
        if ct.values_list('listedPatients3', flat=True).exists():
            filledslots.remove(3)
        if ct.values_list('listedPatients4', flat=True).exists():
            filledslots.remove(4)
        if ct.values_list('listedPatients5', flat=True).exists():
            filledslots.remove(5)
        if ct.values_list('listedPatients6', flat=True).exists():
            filledslots.remove(6)
        return filledslots

    def addorremove_patient(self, addorremove):
        username_value = self.patient_username.text
        password_value = self.patient_password.text

        self.patient_username.text = ''
        self.patient_password.text = ''





        '''
        also make an if else statement that checks if the caretaker has 6 patients already (maximum)
        '''
        global global_caretaker_name
        ct = Caretaker.objects.all().filter(caretakerFullName = global_caretaker_name)

        if addorremove == 'add':
            if validate(self.patient_username.text, self.patient_password.text) == True:
                avalibleslots = checkslots(global_caretaker_name)
                avalibleslots_len = len(avalibleslots)
                if avalibleslots_len == 0:
                    error(1) # IF THERE ARE NO AVALIBLE SLOTS
                else:
                    if avalibleslots[0] == 1:
                        Caretaker.objects.filter(caretakerFullName=global_caretaker_name).update(listedPatients=self.patient_username.text)
                    if avalibleslots[0] == 2:
                        Caretaker.objects.filter(caretakerFullName=global_caretaker_name).update(listedPatients2=self.patient_username.text)
                    if avalibleslots[0] == 3:
                        Caretaker.objects.filter(caretakerFullName=global_caretaker_name).update(listedPatients3=self.patient_username.text)
                    if avalibleslots[0] == 4:
                        Caretaker.objects.filter(caretakerFullName=global_caretaker_name).update(listedPatients4=self.patient_username.text)
                    if avalibleslots[0] == 5:
                        Caretaker.objects.filter(caretakerFullName=global_caretaker_name).update(listedPatients5=self.patient_username.text)
                    if avalibleslots[0] == 6:
                        Caretaker.objects.filter(caretakerFullName=global_caretaker_name).update(listedPatients6=self.patient_username.text)
            else:
                error(1) # IF THE USERNAME AND PASSWORD DOESN'T EXIST / DOESN'T MATCH


        elif addorremove == 'remove':
            if validate(self.patient_username.text, self.patient_password.text) == True:
                filledslots = checkfilledslots(global_caretaker_name)
                usedslots_len = len(filledslots)
                if usedslots_len == 0:
                    error(1) # IF THERE ARE NO AVALIBLE SLOTS
                else:
                    if ct.values_list('listedPatients', flat=True).exists():
                        lpat = ct.values_list('listedPatients', flat=True)[0]
                        if lpat == self.patient_username.text:
                            Caretaker.objects.filter(caretakerFullName=global_caretaker_name).update(listedPatients='')
                    if ct.values_list('listedPatients2', flat=True).exists():
                        lpat = ct.values_list('listedPatients2', flat=True)[0]
                        if lpat == self.patient_username.text:
                            Caretaker.objects.filter(caretakerFullName=global_caretaker_name).update(listedPatients2='')
                    if ct.values_list('listedPatients3', flat=True).exists():
                        lpat = ct.values_list('listedPatients3', flat=True)[0]
                        if lpat == self.patient_username.text:
                            Caretaker.objects.filter(caretakerFullName=global_caretaker_name).update(listedPatients3='')
                    if ct.values_list('listedPatients4', flat=True).exists():
                        lpat = ct.values_list('listedPatients4', flat=True)[0]
                        if lpat == self.patient_username.text:
                            Caretaker.objects.filter(caretakerFullName=global_caretaker_name).update(listedPatients4='')
                    if ct.values_list('listedPatients5', flat=True).exists():
                        lpat = ct.values_list('listedPatients5', flat=True)[0]
                        if lpat == self.patient_username.text:
                            Caretaker.objects.filter(caretakerFullName=global_caretaker_name).update(listedPatients5='')
            else:
                error(1)

class windowManager(ScreenManager):
    pass

class tapSpeechApp(App):
    #kv = Builder.load_file("tapspeech.kv")
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
        self.sm.add_widget(en_updatepatientlistScreen(name="en_updatepatientlist"))
        self.sm.add_widget(ct_welcomeScreen(name="ct_welcome"))
        self.sm.add_widget(ct_loginScreen(name="ct_login"))
        self.sm.add_widget(ct_registerScreen(name="ct_register"))
        self.sm.add_widget(ct_patientUpScreen(name="ct_patientUp"))
        self.sm.add_widget(ct_patientDownScreen(name="ct_patientDown"))
        self.sm.add_widget(ct_contactsScreen(name="ct_contacts"))
        self.sm.add_widget(ct_caretakerUpScreen(name="ct_caretakerUp"))
        self.sm.add_widget(ct_caretakerDownScreen(name="ct_caretakerDown"))
        self.sm.add_widget(ct_informationScreen(name="ct_information"))
        self.sm.add_widget(ct_updatepatientlistScreen(name="ct_updatepatientlist"))
        self.sm.current = "en_welcome"
        return self.sm

if __name__ == '__main__':
    tapSpeechApp().run()
