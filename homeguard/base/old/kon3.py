#!/usr/bin/python

import RPi.GPIO as GPIO
import time
import smtplib
import datetime
import linecache
#import MySQLdb

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

#def insert_to_db(value):
#        db = MySQLdb.connect(host = "89.76.123.181", user = "malinka", passwd = "123123123", db = "hssystem")       cur = db.cursor()
 #       params = [value]
#       print (params)
  #      try:
   #             cur.execute("INSERT INTO hssystem.kontrakton (data, Wartosc) VALUES (NOW(),%s)", params)
    #            db.commit()
     #           print ("Dodano do bazy")
      #  except MySQLdb.Error, e:
        #        print ("Wystapil blad. %s" %e)
        #finally:
          #      cur.close()
           #     db.close()


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
                        sendEmail()
                        appendFile(timestamp)
             #           insert_to_db(door)
                        time.sleep(9)
                else:
                        door = doorState[0]
                        print (door)
                        timestamp = getTime()
              #          insert_to_db(door)
                        time.sleep(5)

if __name__=='__main__':
                try:
                   main()
                   pass
                except KeyboardInterrupt:
                   pass
GPIO.cleanup()




