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



    # def request_puller(name):
    #     names = name
    #     broken_names = []
    #
    #     len_name = len(names)
    #     timer0 = 0
    #     for i in range(len_name):
    #         reqs = Requests.objects.all().filter(request_patient__in=names[timer0])
    #         len_reqs = len(reqs)
    #         if len_reqs == 0:
    #             broken_names.append(names[timer0])
    #         timer0 =+ 1
    #
    #     len_broken_names = len(broken_names)
    #     timer0 = 0
    #     for i in range(len_broken_names):
    #         names.remove(broken_names[timer0])
    #         timer0 =+ 1
    #
    #
    #     reqs = Requests.objects.all().filter(request_patient__in=names)
    #     lenreq = len(reqs)
    #
    #     context = reqs.distinct().order_by('-request_time')
    #     context_len = len(context)
    #     timer = 0
    #     for i in range(context_len):
    #         r_pat = context.values_list('request_patient', flat=True)[timer]
    #         r_type = context.values_list('request_type', flat=True)[timer]
    #         r_spec = context.values_list('request_specification', flat=True)[timer]
    #         r_time = context.values_list('request_time', flat=True)[timer]
    #         print(r_pat + " " + r_type + " "  + r_spec + " "  + r_time)
    #         if timer == 0:
    #             request0 = {timer: {r_pat, r_type, r_spec, r_type}}
    #         elif timer == 1:
    #             request1 = {timer: {r_pat, r_type, r_spec, r_type}}
    #         elif timer == 2:
    #             request2 = {timer: {r_pat, r_type, r_spec, r_type}}
    #         timer=+1
    #         if timer == 2:
    #             print(request0)
    #             print(request1)
    #             print(request2)
    #
    # def request_validator(name):
    #     reqs = Requests.objects.all().filter(request_patient__in=name)
    #     if len(reqs) == 0:
    #         return False

    def request_puller(name):
        names = name
        reqs = Requests.objects.all().filter(request_patient__in=names)
        context = reqs.distinct().order_by('-request_time')[:3]
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
    print(reqlist[0][0])


print(" ")
print("Which Command would you like to test?")
print("account_creation, account_search, request_pull")
x = input()
if x == "account_creation":
    account_creation()
elif x == "account_search":
    account_search()
elif x == "request_pull":
    request_pull()
