#!/usr/bin/python

import RPi.GPIO as GPIO
import time
import smtplib
import datetime
import linecache

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
def main():
        #init()
        while True:
                if GPIO.input(door_pin):
                   print ('Drzwi otwarte')
                   now = datetime.datetime.now()
                   test = now.strftime("%Y-%m-%d %H:%M:%S")
                   print (test)
                   sendEmail()
                   appendFile(test)
                   time.sleep(9)
                else:
                   print ('Drzwi zamkniete')
                   time.sleep(5)
if __name__=='__main__':
                try:
                   main()
                   pass
                except KeyboardInterrupt:
                   pass
GPIO.cleanup()
