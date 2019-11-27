import RPi.GPIO as GPIO
import time
import smtplib
import datetime




smtpUser = 'ZPItest1111@gmail.com'
smtpPass = 'ZPItest1'
toAdd = 'laizer96@gmail.com'
fromAdd = smtpUser

subject = 'Wylacz gaz'
header = 'Do: ' + toAdd + '\n'  + 'Od: ' + fromAdd + '\n' + 'Temat: ' + subject
body = 'Wylac gaz '

SPICLK = 11
SPIMISO = 9
SPIMOSI = 10
SPICS = 8
mq7_dpin = 26
mq7_apin = 0

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
#main ioop
file = open ('gas.txt', 'w+')


def sendEmail():
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(smtpUser, smtpPass)
    s.sendmail(fromAdd, toAdd, header + '\n' + body)
    s.quit()

def appendFile(now):
        file = open("log.txt", "a+")
        file.write(now + " Drzwi otwarte \r\n")
        file.close()


def main():
         init()
         print("Prosze czekac...")
         time.sleep(20)
         while True:
                  COlevel=readadc(mq7_apin, SPICLK, SPIMOSI, SPIMISO, SPICS)
                  if GPIO.input(mq7_dpin):
                          print("Nie wykryto CO")
                          time.sleep(0.5)

                  else:
                          print("Wykryto CO")
                          print("Zmierzona wartosc napiecia = " + str("%.2f" % ((COlevel / 1024.) * 5)) + " V")
                          print("Procent CO w powietrzu: " + str("%.2f" % ((COlevel / 1024.) * 100)) + " %")
                          now = datetime.datetime.now()
                          test = now.strftime("%Y-%m-%d %H:%M:%S")
                          print (test)
                          sendEmail()
                          #appendFile(test)
                          time.sleep(10)
if __name__ =='__main__':
         try:
                  main()
                  pass
         except KeyboardInterrupt:
                  pass

GPIO.cleanup()
