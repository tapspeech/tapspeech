import os
import django
import sqlite3
import pandas as pd
from datetime import datetime
import pytz

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tapSpeech.settings')
django.setup()

from tapSpeech_app.models import Patient, Requests

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

    def check_infos(name, birthday):
        #list to store emails
        names=[]
        birthdays=[]
        namecheck = False
        birthdatecheck = False
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
                        print("Successful, Account is real.")
                else:
                    print("Birthdate Check Failed")
            else:
                print("Name Check Failed")

    def request_puller(name):
        names = name
        reqs = Requests.objects.all().filter(request_patient__in=names)
        context = reqs.distinct().order_by('-request_time')[:3]
        requests_exists = True
        if context.values_list('request_patient', flat=True).exists():
            context_len = len(context)
            timer = 0
            reqlist = []
            for i in range(context_len):
                r_pat = context.values_list('request_patient', flat=True)[timer]
                r_type = context.values_list('request_type', flat=True)[timer]
                r_spec = context.values_list('request_specification', flat=True)[timer]
                r_time = context.values_list('request_time', flat=True)[timer]
                print(r_pat + " " + r_type + " "  + r_spec + " "  + r_time)
                if timer == 0:
                    req0 = [r_pat, r_type, r_spec, r_time]
                    reqlist.append(req0)
                elif timer == 1:
                    req1 = [r_pat, r_type, r_spec, r_time]
                    reqlist.append(req1)
                elif timer == 2:
                    req2 = [r_pat, r_type, r_spec, r_time]
                    reqlist.append(req2)
                timer=+1
            return reqlist
        else:
            requests_exists = False
            return requests_exists

    def econtact_check(name):
        pat = Patient.objects.all().filter(patientFullName=name)
        econ1 = pat.values_list('patientEmergencyContact', flat=True)[0]
        econ2 = pat.values_list('patientEmergencyContact2', flat=True)[0]
        econ3 = pat.values_list('patientEmergencyContact3', flat=True)[0]
        print(econ1 + " "  + econ2 + " " + econ3)

def account_creation():
    print(" ")
    print("---- Account Creation ----")
    x = input("input name pls ")
    y = input("input birthdate pls ")


    new_patient = Patient(patientFullName = x, patientBirthDate = y)
    new_patient.save()


def account_search():
    print(" ")
    print("---- Account Search ----")
    name = input("input name pls ")
    birthday = input("input birthdate pls ")
    info_response = ReadSQL.check_infos(name, birthday)
    print(info_response)

def request_pull():
    print(" ")
    print("---- Request Search ----")
    searchnamelist = []
    name1 = input("input name 1 pls ")
    searchnamelist.append(name1)
    name2 = input("input name 2 pls ")
    searchnamelist.append(name2)
    print(searchnamelist)
    reqlist = ReadSQL.request_puller(searchnamelist)
    if reqlist == False:
        print('No Functions')
    else:
        print(reqlist[0][0])

def check_econtacts():
    print(" ")
    print("---- Emergency Contact Search ----")
    name = input("input name pls ")
    ReadSQL.econtact_check(name)


print(" ")
print("Which Command would you like to test? (type the number)")
print("1) account_creation, 2) account_search, 3) request_pull, 4) check_emer_contacts")
x = input()
if x == "1":
    account_creation()
elif x == "2":
    account_search()
elif x == "3":
    request_pull()
elif x == "4":
    check_econtacts()
