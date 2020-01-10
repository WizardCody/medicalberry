import sys
import os
from core.base import MiBand2
from bluepy.btle import BTLEException
from django.utils import timezone

import linecache
import smtplib

wiersz1 = linecache.getline('haslo.txt',1)
wiersz2 = linecache.getline('haslo.txt',2)
wiersz3 = linecache.getline('haslo.txt',3)

smtpUser = wiersz1.strip()
smtpPass = wiersz2.strip()
toAdd = wiersz3.strip()
fromAdd = smtpUser.strip()

def sendEmail(body):

    subject = 'Medicalberry warning!'

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(str(smtpUser), str(smtpPass))
    
    from email.message import EmailMessage
    
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['To'] = toAdd
    msg['From'] = fromAdd
    msg.set_content(body)
    
    s.send_message(msg)
    print ('E-mail has been sent')
    s.quit()

import requests

def telegram_bot_sendtext(bot_message):
        
    #bot_token - api token
    bot_token = '848324519:AAF2Q1Jwf8VcfuiZUw0dhmcW8OUZm4B6o7A'
    #bot_chatID - recivers ID
    bot_chatID = '-336603765'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
    
    response = requests.get(send_text)

    return response.json()

# PARENT DIRECTORY PATH
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "medicalberry.settings")

import django
django.setup()

from heartguard.models import Device, Heartrate

# GET DEVICE
current_Device = Device.objects.get(id=1)

def send_to_db(rate):

    # GET DEVICE
    current_Device.refresh_from_db()

    hr = Heartrate(device=current_Device, value=rate, event_time=timezone.now())
    
    if rate > current_Device.patient.max_heartrate:
        hr.status = False
        warning = ("Heartrate too high!\npatient: " + str(current_Device.patient) + "\ndevice: " + str(current_Device).replace("_"," ") + "\nrate: " + str(rate))
        
        
        if current_Device.patient.notify_telegram:
            telegram_bot_sendtext(warning)
            
        if current_Device.patient.notify_mail:
            sendEmail(warning)
            
    elif rate < current_Device.patient.min_heartrate:
        hr.status = False
        warning = ("Heartrate too low!\npatient: " + str(current_Device.patient) + "\ndevice: " + str(current_Device).replace("_"," ") + "\nrate: " + str(rate))
        
        if current_Device.patient.notify_telegram:
            telegram_bot_sendtext(warning)
            
        if current_Device.patient.notify_mail:
            sendEmail(warning)
    
    hr.save()
    print(hr)

while True:
    try:
        band = MiBand2(current_Device.MAC_address, debug=True)
        band.setSecurityLevel(level="medium")
        band.authenticate()
        band.start_heart_rate_realtime(heart_measure_callback=send_to_db)
        band.disconnect()
    except BTLEException:
        pass
