import requests
from os.path import isfile, join
import string
from os import listdir
import os
import imghdr
from selenium import webdriver
from email.message import EmailMessage
from datetime import date
import smtplib
import pytesseract
import base64
import time
from copy_to_clipboard import copy_to_clipboard as copy_clip
from Timetable import *
import inspect


attachement = False
today = date.today()
folder_path = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))+f"/{str(today)}"
options = webdriver.ChromeOptions()

# setting folder path for saving attachments
preferences = {"download.default_directory": folder_path}
options.add_experimental_option("prefs", preferences)
ind = 0
web = webdriver.Chrome(chrome_options=options)
web.get("<PORTAL URL>")
for i in range(5):
    web.get("<PORTAL URL>")
    time.sleep(2)
    admin_no = "ADMISSON NO"
    password = "PASSWORD"
    admin_input = web.find_element_by_name(
        "ctl00$ContentPlaceHolder1$txtusername")
    admin_input.send_keys(admin_no)

    pass_input = web.find_element_by_name("ctl00$ContentPlaceHolder1$txtpwd")
    pass_input.send_keys(password)

    ele_captcha = web.find_element_by_xpath(
        '//*[@id="ContentPlaceHolder1_imgCaptcha"]')
    img_captcha_base64 = web.execute_async_script("""
            var ele = arguments[0], callback = arguments[1];
            ele.addEventListener('load', function fn(){
              ele.removeEventListener('load', fn, false);
              var cnv = document.createElement('canvas');
              cnv.width = this.width; cnv.height = this.height;
              cnv.getContext('2d').drawImage(this, 0, 0);
              callback(cnv.toDataURL('image/jpeg').substring(22));
            }, false);
            ele.dispatchEvent(new Event('load'));
            """, ele_captcha)
    with open(r"captcha.jpg", 'wb') as f:
        f.write(base64.b64decode(img_captcha_base64))
    captcha_text_temp = pytesseract.image_to_string("captcha.jpg")
    captcha_text = ""
    for k in captcha_text_temp:
        if(k in string.ascii_uppercase or k in string.digits or k in string.ascii_lowercase):
            captcha_text += k
    captcha_input = web.find_element_by_name(
        "ctl00$ContentPlaceHolder1$txtCaptcha")
    captcha_input.send_keys(captcha_text)
    login_btn = web.find_element_by_name("ctl00$ContentPlaceHolder1$btnLogin")
    login_btn.click()
    print(f"Try {ind+1}")
    ind += 1
    if(web.current_url == "<PORTAL URL>home/home.aspx"):
        break
print("Successfully logged in to SRM!")

# Going to Schedule
schedule_btn = web.find_element_by_name(
    "ctl00$ctl00$ContentPlaceHolder1$ContentPlaceHolder2$btnschedule")
schedule_btn.click()


# Deleting Files
mypath = f"{today}"
if(os.path.exists(mypath)):
    files2 = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    print(files2)
    for k in files2:
        if os.path.exists(f"{today}/{k}"):
            os.remove(f"{today}/{k}")
else:
    pass

# Fetching Data
row_count = len(web.find_elements_by_xpath(
    "//*[@id='ContentPlaceHolder1_ContentPlaceHolder2_Gv']/tbody/tr"))
colum_count = len(web.find_elements_by_xpath(
    '//*[@id="ContentPlaceHolder1_ContentPlaceHolder2_Gv"]/tbody/tr[1]/th'))

lst = []
for i in range(2, row_count+1):

    templst = []
    for k in range(1, colum_count+1):
        tempxpath = '//*[@id="ContentPlaceHolder1_ContentPlaceHolder2_Gv"]/tbody/tr[' + \
            str(i)+']/td['+str(k)+']'
        temp = web.find_element_by_xpath(tempxpath).text

        if(k == 5 and temp != ''):
            if temp.find("drive") == -1:
                file_btn = web.find_element_by_link_text(temp)
                file_btn.click()
                attachement = True
            else:
                templst.append(temp)
        else:
            templst.append(temp)
    lst.append(templst)

lst2 = lst
for k in range(len(lst)):
    lst2[k] = '\n'.join(lst[k])

current_date_lst = str(today).split("-")
current_date = " ".join(current_date_lst[::-1])
schedule = time_table[findDay(current_date)] + '\n' + last_updated + \
    '\n\n---------------------------\n\n' + 'Links:'


schedule += '\n\n'
schedule += '\n*********\n\n'.join(lst2)


f = open("schedule.txt", 'w')
f.write(schedule)
f.close()


file = open("schedule.txt", 'r+')
body = file.read()
file.close()

# Creating a new Email message
msg = EmailMessage()
msg['Subject'] = f"Class Schedule for {today}"
msg['From'] = "SENDER'S EMAIL HERE"
msg['To'] = "RECIEVER'S EMAIL HERE"
msg.set_content(str(body))
passemail = "PASSWORD"
if attachement == True:
    time.sleep(10)
    web.quit()
    mypath = f"{today}"
    files = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    for k in files:
        filelst = k.split(".")
        if(filelst[1] == "jpg" or filelst[1] == "jpeg" or filelst[1] == "png"):
            with open(f"{today}/{k}", 'rb') as f:
                file_data = f.read()
                file_type = imghdr.what(f.name)
                file_name = f.name
                msg.add_attachment(file_data, maintype='image',
                                   subtype=file_type, filename=k)
        else:
            with open(f"{today}/{k}", 'rb') as f:
                file_data = f.read()
                file_name = f.name
                msg.add_attachment(file_data, maintype='application',
                                   subtype='octet-stream', filename=k)

else:
    web.quit()

# Sending  Email
with smtplib.SMTP_SSL('smtp.gmail.com', 465)as server:
    server.login("SENDERS EMAIL HERE", passemail)
    print("Login Success!")
    server.send_message(msg)
    print("Schedule Sent!")
    
# Copy to clipboard for sharing
copy_clip()
