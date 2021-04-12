from __future__ import print_function
from flask import *
import os
import calendar
import time
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import re
import time
from selenium import webdriver

app = Flask(__name__)

app.secret_key = 'd10wcb'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''


#DRIVER CODE

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/classroom.announcements']


creds = None
# The file token.json stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.json', 'w') as token:
        token.write(creds.to_json())

service = build('classroom', 'v1', credentials=creds)

#Classroom IDs

# Courses:
# D10A_Python Mini Project 2020-21(Even Semester)
# 311214833912
# -----------------

# OS/INFT/D10A/Sem-IV(2020-21) (USE THIS)
# 259650746659
# -----------------

# D10A EM IV 20-21
# 259569119725
# -----------------

# D10A-AT-AY 20-21
# 259551344177
# -----------------

# D10A COA (USE THIS)
# 246181325204
# -----------------

# Computer Network and Network Design
# 259426553110
# -----------------

# Python Lab 2020-21
# 259427016989
# -----------------

#CREATE TWO EMPTY LISTS

announcement_list_COA = []
announcement_list_OS = []

# Call the Classroom API

#COA Classroom
announcements_COA = service.courses().announcements()
response_COA = announcements_COA.list(courseId=246181325204).execute()
announcement_dict_COA = response_COA.get("announcements")

for announcement in announcement_dict_COA:
    announcement_list_COA.append(announcement['text'])

#-----

#OS Classroom
announcements_OS = service.courses().announcements()
response_OS = announcements_OS.list(courseId=259650746659).execute()
announcement_dict_OS = response_OS.get("announcements")


for announcement in announcement_dict_OS:
    announcement_list_OS.append(announcement['text'])



#MATCH MEET LINKS
#MATHS - https://meet.google.com/fsx-wnbm-iqs
#CNND - https://meet.google.com/nzs-ynjs-bfu
#Python Lab - https://meet.google.com/ryi-ndgr-omj
#AT - https://meet.google.com/ieh-hhaz-mdm

coa_string_part1 = "Join for COA - "
coa_link = ""

os_string_part1 = "Join for OS - "
os_link = ""

for line in announcement_list_OS:
    line = line.rstrip()
    if re.match("^https://meet\S+", line):
        os_link = line[0:36]
        break

for line in announcement_list_COA:
    line = line.rstrip()
    if re.match("^https://meet\S+", line):
        coa_link = line[0:36]
        break


final_string_math = "Join for Maths - https://meet.google.com/fsx-wnbm-iqs"
final_string_cnnd = "Join for CNND - https://meet.google.com/nzs-ynjs-bfu"
final_string_pyt = "Join for Python Lab - https://meet.google.com/ryi-ndgr-omj"
final_string_at = "Join for AT - https://meet.google.com/ieh-hhaz-mdm"

final_string_os = os_string_part1 + os_link
final_string_coa = coa_string_part1 + coa_link

# PRINT STATEMENTS FOR TESTING

# print("1. Maths")
# print("2. Computer Networks and Network Design")
# print("3. Python Lab")
# print("4. Automata Theory")
# print("5. Operating Systems")
# print("6. Computer Organization and Architecture")
# choice = int(input("Enter your choice:"))

# if choice == 1:
#     final_string = final_string_math
# elif choice ==2:
#     final_string = final_string_cnnd
# elif choice ==3:
#     final_string = final_string_pyt
# elif choice ==4:
#     final_string = final_string_at
# elif choice ==5:
#     final_string = final_string_os
# elif choice ==6:
#     final_string = final_string_coa
# else: 
#     print("Invalid Input")


#-------------------------------------

#SEND MESSAGE OVER WHATSAPP

def send_message_on_whatsapp(final_string):
    #ADDING WEB DRIVER
    str1 = final_string
    options = webdriver.ChromeOptions()
    

    web_driver = webdriver.Chrome(executable_path = 'D:\Downloads\chromedriver_win32\chromedriver.exe')

    web_driver.get("https://web.whatsapp.com")

    time.sleep(10)

    #Find Group Name

    user_name = 'Ninad Rao'
    user = web_driver.find_element_by_xpath('//span[@title="{}"]'.format(user_name))
    user.click()

    message = web_driver.find_element_by_xpath('//div[@class="_2A8P4"]')
    message.send_keys(str1)


    message_submit = web_driver.find_element_by_xpath('//button[@class="_1E0Oz"]')
    message_submit.click()

    time.sleep(10)

    web_driver.close()


# --------------- ROUTES --------------------

@app.route('/')
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/lec_maths')
def lec_maths():
    final_string = final_string_math
    send_message_on_whatsapp(final_string)
    flash('Message Sent')
    return render_template('dashboard.html')

@app.route('/lec_cnnd')
def lec_cnnd():
    final_string = final_string_cnnd
    send_message_on_whatsapp(final_string)
    flash('Message Sent')
    return render_template('dashboard.html')

@app.route('/lec_python')
def lec_python():
    final_string = final_string_pyt
    send_message_on_whatsapp(final_string)
    flash('Message Sent')
    return render_template('dashboard.html')

@app.route('/lec_automata')
def lec_automata():
    final_string = final_string_at
    send_message_on_whatsapp(final_string)
    flash('Message Sent')
    return render_template('dashboard.html')

@app.route('/lec_os')
def lec_os():
    final_string = final_string_os
    send_message_on_whatsapp(final_string)
    flash('Message Sent')
    return render_template('dashboard.html')

@app.route('/lec_coa')
def lec_coa():
    final_string = final_string_coa
    send_message_on_whatsapp(final_string)
    flash('Message Sent')
    return render_template('dashboard.html')


if __name__ == '__main__':
    app.run(debug=True)