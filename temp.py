#!/usr/bin/python

import RPi.GPIO as GPIO
import time
import smtplib
import datetime
import linecache
import os, sys
import requests


# DJANGO setup
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "medicalberry.settings")

import django
django.setup()

from homeguard.models import Device, Kontrakton

current_Device = Device.objects.get(pk=1)

from django.utils import timezone


wiersz1 = linecache.getline('haslo.txt',1)
wiersz2 = linecache.getline('haslo.txt',2)
wiersz3 = linecache.getline('haslo.txt',3)

smtpUser = wiersz1.strip()
smtpPass = wiersz2.strip()
toAdd = wiersz3.strip()
fromAdd = smtpUser.strip()

subject = 'Medicalberry warning!'
header = 'Do: ' + toAdd + '\n'  + 'Od: ' + fromAdd + '\n' + 'Temat: ' + subject
body = 'Close your doors'

door_pin = 21

GPIO.setmode(GPIO.BCM)
GPIO.setup(door_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

doorState = ["Doors are closed", "Doors are open"]

def sendEmail():

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
        
def telegram_bot_sendtext(bot_message):
    
    #bot_token - api token
    bot_token = '848324519:AAF2Q1Jwf8VcfuiZUw0dhmcW8OUZm4B6o7A'
    #bot_chatID - recivers ID
    bot_chatID = '-336603765'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)

    return response.json()

def main():
        #init()
        while True:
                if GPIO.input(door_pin):
                        door = doorState[1]
                        print (door)
                        sendEmail()
                        print(Kontrakton.objects.all())
                        Kontrakton(device=current_Device, value=True, event_time=timezone.now()).save()
                        telegram_message = telegram_bot_sendtext("Warning! Some windows are open! Check medicalberry panel!")
                        print(telegram_message)
                        time.sleep(60)
                else:
                        door = doorState[0]
                        print (door)
                        print (Kontrakton.objects.all())
                        Kontrakton(device=current_Device, value=False, event_time=timezone.now()).save()
                        time.sleep(60)
    
if __name__=='__main__':
                try:
                   main()
                   pass
                except KeyboardInterrupt:
                   pass
GPIO.cleanup()



