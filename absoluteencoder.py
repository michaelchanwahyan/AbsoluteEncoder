#from datetime import datetime
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

PIN_CLK = 2
PIN_DAT = [3,14]
PIN_CS  = 4
delay = 0.0000005
ns = 2 # number of sensors attached
# totally 10 bits to be extracted from SSI signal
bitcount = 16

# pin setup done here
try:
    GPIO.setup(PIN_CLK,GPIO.OUT)
    GPIO.setup(PIN_DAT[:],GPIO.IN)
    GPIO.setup(PIN_CS,GPIO.OUT)                                                                                                    
    GPIO.output(PIN_CS,1)
    GPIO.output(PIN_CLK,1)
except:
    print "ERROR. Unable to setup the configuration requested"                                     

#wait some time to start
time.sleep(0.5)

print "GPIO configuration enabled"

def clockup():
    GPIO.output(PIN_CLK,1)
def clockdown():
    GPIO.output(PIN_CLK,0)
def MSB():
    # Most Significant Bit
    clockdown()

def readpos():
    GPIO.output(PIN_CS,0)
    time.sleep(delay)
    MSB()
    data = [0]*ns
    
    for i in range(0,bitcount):
        if i > 1 :
            #print i
            clockup()
            time.sleep(delay)
            for j in range(0,ns):
                data[j] <<= 1  
                data[j] |=  GPIO.input(PIN_DAT[j])
            clockdown()
            time.sleep(delay)
        else :
            clockup()
            time.sleep(delay)
            clockdown()
            time.sleep(delay)
       # else:
       #     for k in range(0,6):
       #         clockup()
       #         clockdown()
    GPIO.output(PIN_CS,1)
    return data
    time.sleep(0.00001)

try:
    while(1):
        print readpos()
        #data=readpos()
        #print datetime.now().strftime("%H%M%S"), data
        time.sleep(0.001)
        #break
        
finally:
    print "cleaning up GPIO"
    GPIO.cleanup()
