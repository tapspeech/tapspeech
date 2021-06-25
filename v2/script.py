import os
import django
import sqlite3
import pandas as pd

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tapSpeech.settings')
django.setup()

from tapSpeech_app.models import Patient

print("---- Account Creation ----")
x = input("input name pls ")
y = input("input birthdate pls ")


new_patient = Patient(patientFullName = x, patientBirthDate = y)
new_patient.save()

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

print("---- Database Search ----")
changestest = input("Would you like to try and look for the account in the database? ")
if changestest == "yes":
    name = input("input name pls ")
    birthday = input("input birthdate pls ")
    info_response = ReadSQL.check_infos(name, birthday)
    print(info_response)
else:
    print("Script Ended")
