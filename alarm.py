import RPi.GPIO as GPIO
import time
from pir import Pir
from motor import Motor
global pins
pins = [18,20,22,24] # controller inputs: in1, in2, in3, in4

def buzzer(BUZZER):
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    #BUZZER= 13
    buzzState = True
    GPIO.setup(BUZZER, GPIO.OUT)
    for i in range (3):
        GPIO.output(BUZZER, buzzState)
        time.sleep(.1)
        GPIO.output(BUZZER, False)

class Alarm():

  def __init__(self, pir, led):
    self.alarm = Pir(pir, led)
  
  def setup(self, led):
    GPIO.output(led, GPIO.LOW)
    print ("Sensor initializing . . .")
    #time.sleep(30) #Give sensor time to startup
    print ("50% . . .")
    time.sleep(30) #Give sensor time to startup
    print ("Active")
    print ("Press Ctrl+c to end program")
    GPIO.output(led, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(led, GPIO.LOW)

  
  def runAlarm(self, pir, led):
    stepper = Motor(pins)
    try:
      while True:
        stepper.loop(cw)
        stepper.loop(ccw)
        if GPIO.input(pir) == True: #If PIR pin goes high, motion is detected
          print ("Motion Detected!")
          buzzer(13)
          print("Buzzer on")
          GPIO.output(led, GPIO.HIGH) #Turn on LED
          time.sleep(3) #Keep LED on for 3 seconds
          print ("led on!")
          GPIO.output(led, GPIO.LOW) #Turn off LED
          time.sleep(.1)
    
    except KeyboardInterrupt: #Ctrl+c
      pass #Do nothing, continue to finally
    GPIO.cleanup() 
    print ("Program ended")


pir = 23 #Assign pin 8 to PIR
led = 21 #Assign pin 10 to LED
security = Alarm(pir,led)
security.setup(led)
security.runAlarm(pir, led)





  

  

