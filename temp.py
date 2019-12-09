#!/usr/bin/python

import RPi.GPIO as GPIO
import time
import smtplib
import datetime
import linecache
import os, sys

# PARENT DIRECTORY PATH
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "medicalberry.settings")

import django
django.setup()

from homeguard.models import Device, Kontrakton

# PRINT ALL HEARTRATES

# GET DEVICE
current_Device = Device.objects.get(pk=1)

from django.utils import timezone

wiersz1 = linecache.getline('haslo.txt',1)
wiersz2 = linecache.getline('haslo.txt',2)
wiersz3 = linecache.getline('haslo.txt',3)

smtpUser = wiersz1
smtpPass = wiersz2
toAdd = wiersz3
fromAdd = smtpUser

subject = 'Test otwartych drzwi'
header = 'Do: ' + toAdd + '\n'  + 'Od: ' + fromAdd + '\n' + 'Temat: ' + subject
body = 'Zamknij drzwi'

door_pin = 21

GPIO.setmode(GPIO.BCM)
GPIO.setup(door_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

file = open("log.txt","w+")

doorState = ["Drzwi zamkniete", "Drzwi otwarte"]

def sendEmail():
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.ehlo()
        s.starttls()
        s.ehlo()
        s.login(smtpUser, smtpPass)
        s.sendmail(fromAdd, toAdd, header + '\n' + body)
        s.quit()

def appendFile(now):
        file = open("log.txt","a+")
        file.write(now + " Drzwi otwarte \r\n")
        file.close()

def getTime():
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        print(timestamp)
        return timestamp

def main():
        #init()
        while True:
                if GPIO.input(door_pin):
                        door = doorState[1]
                        print (door)
                        timestamp = getTime()
                        sendEmail()
                        appendFile(timestamp)
                        print(Kontrakton.objects.all())
                        Kontrakton(device=current_Device, value=True, event_time=timezone.now()).save()
                        time.sleep(60)
                else:
                        door = doorState[0]
                        print (door)
                        timestamp = getTime()
                        print(Kontrakton.objects.all())
                        Kontrakton(device=current_Device, value=False, event_time=timezone.now()).save()
                        time.sleep(60)

if __name__=='__main__':
                try:
                   main()
                   pass
                except KeyboardInterrupt:
                   pass
GPIO.cleanup()




