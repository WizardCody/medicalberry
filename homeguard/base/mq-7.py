import RPi.GPIO as GPIO
import time
import smtplib
import datetime
import linecache
import os, sys
import requests

wiersz1 = linecache.getline('haslo.txt',1)
wiersz2 = linecache.getline('haslo.txt',2)
wiersz3 = linecache.getline('haslo.txt',3)

smtpUser = wiersz1
smtpPass = wiersz2
toAdd = wiersz3
fromAdd = smtpUser


#pins setup
SPICLK = 11
SPIMISO = 9
SPIMOSI = 10
SPICS = 8
mq7_dpin = 26
mq7_apin = 0


# DJANGO setup
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "medicalberry.settings")

import django
django.setup()

from homeguard.models import Device, Gas

current_Device = Device.objects.get(pk=2)

from django.utils import timezone

#port init
def init():
         GPIO.setwarnings(False)
         GPIO.cleanup()                 #clean up at the end of your script
         GPIO.setmode(GPIO.BCM)         #to specify whilch pin numbering system
         # set up the SPI interface pins
         GPIO.setup(SPIMOSI, GPIO.OUT)
         GPIO.setup(SPIMISO, GPIO.IN)
         GPIO.setup(SPICLK, GPIO.OUT)
         GPIO.setup(SPICS, GPIO.OUT)
         GPIO.setup(mq7_dpin,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)

#read SPI data from MCP3008(or MCP3204) chip,8 possible adc's (0 thru 7)
def readadc(adcnum, clockpin, mosipin, misopin, cspin):
        if ((adcnum > 7) or (adcnum < 0)):
                return -1
        GPIO.output(cspin, True)
        GPIO.output(clockpin, False)  # start clock low
        GPIO.output(cspin, False)     # bring CS low
        commandout = adcnum
        commandout |= 0x18  # start bit + single-ended bit
        commandout <<= 3    # we only need to send 5 bits here
        for i in range(5):
                if (commandout & 0x80):
                        GPIO.output(mosipin, True)
                else:
                        GPIO.output(mosipin, False)
                commandout <<= 1
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)

        adcout = 0
        # read in one empty bit, one null bit and 10 ADC bits
        for i in range(12):
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)
                adcout <<= 1
                if (GPIO.input(misopin)):
                        adcout |= 0x1

        GPIO.output(cspin, True)

        adcout >>= 1       # first bit is 'null' so drop it
        return adcout

def sendEmail():
    subject = 'Medicalberry warning!'
    body = 'Gas is releasing'
    
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
         init()
         print("Please wait, Gas sensor is calibrating...")
         time.sleep(20)
         while True:
                  COlevel=readadc(mq7_apin, SPICLK, SPIMOSI, SPIMISO, SPICS)

                  if GPIO.input(mq7_dpin):
                          print("No CO found")
                          time.sleep(1.0)
                  else:
                          print("CO found")
                          print("Voltage value measured = " + str("%.2f" % ((COlevel / 1024.) * 5)) + " V")
                          print("CO in air(%): " + str("%.2f" % ((COlevel / 1024.) * 100)) + " %")
                          sendEmail()
                          telegram_bot_sendtext("Warning! Gas is releasing! Check medicalberry panel!")
                          temp = str("%.2f" % ((COlevel / 1024.) * 100))
                          print("CO in air(%): " + temp + " %")
                          Gas(device=current_Device, value=temp, event_time=timezone.now()).save()  
                          time.sleep(10)
if __name__ =='__main__':
         try:
                  main()
                  pass
         except KeyboardInterrupt:
                  pass

GPIO.cleanup()
