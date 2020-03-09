#!/usr/bin/python

import RPi.GPIO as GPIO
import time
import smtplib
import datetime
import linecache

import os, sys
#import MySQLdb

wiersz1 = linecache.getline('haslo.txt',1)
wiersz2 = linecache.getline('haslo.txt',2)
wiersz3 = linecache.getline('haslo.txt',3)

smtpUser = wiersz1.strip()
smtpPass = wiersz2.strip()
toAdd = wiersz3.strip()
fromAdd = smtpUser.strip()

subject = 'Test otwartych drzwi'
header = 'Do: ' + toAdd + '\n'  + 'Od: ' + fromAdd + '\n' + 'Temat: ' + subject
body = 'Zamknij drzwi'

door_pin = 21

GPIO.setmode(GPIO.BCM)
GPIO.setup(door_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

file = open("log.txt","w+")

doorState = ["Drzwi zamkniete", "Drzwi otwarte"]

#
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "medicalberry.settings")

import django
django.setup()

from homeguard.models import Device, Kontrakton
print(Kontrakton.objects.all())
current_Device = Device.objects.get(pk=1)
from django.utils import timezone

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
                        #now = datetime.datetime.now()
                        #test = now.strftime("%Y-%m-%d %H:%M:%S")
                        #print(test)
                    #    sendEmail()
                    #    appendFile(timestamp)
                        Kontrakton(device=current_Device, value=False, event_time=timezone.now()).save()
             #           insert_to_db(door)
                        time.sleep(9)
                else:
                        door = doorState[0]
                        print (door)
                        timestamp = getTime()
                        Kontrakton(device=current_Device, value=True, event_time=timezone.now()).save()
                        print("asdf")

              #          insert_to_db(door)
                        time.sleep(5)

if __name__=='__main__':
                try:
                   main()
                   pass
                except KeyboardInterrupt:
                   pass
GPIO.cleanup()




