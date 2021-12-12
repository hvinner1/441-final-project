import RPi.GPIO as GPIO
import time
from pir import Pir
from motor import Motor
GPIO.setmode(GPIO.BCM)
import multiprocessing

global pins, cw, ccw
pins = [18,20,22,24] # controller inputs: in1, in2, in3, in4
ccw = [ [1,0,0,0],[1,1,0,0],[0,1,0,0],[0,1,1,0],
        [0,0,1,0],[0,0,1,1],[0,0,0,1],[1,0,0,1] ]
cw = ccw[:]  # use slicing to copy list 
cw.reverse()

def runMotor(): #runs the motor cw and ccw in a loop
  stepper = Motor(pins)
  try:
    while True:
      stepper.loop(cw)
      stepper.loop(ccw)
  except e:
    print(e)
    pass

  GPIO.cleanup()

def buzzer(BUZZER): #turns on the buzzer and beeps 4 times
    GPIO.setwarnings(False)
    #BUZZER= 13
    buzzState = True
    GPIO.setup(BUZZER, GPIO.OUT)
    for i in range (4):               
      GPIO.output(BUZZER, 0)# set output to 0
      time.sleep(0.1)# wait 0.5 sec
      GPIO.output(BUZZER, 1)# set output to 3.3V
      time.sleep(0.1)
      GPIO.output(BUZZER, 0)

class Alarm():

  def __init__(self, pir, led): #create alarm as a pir
    self.alarm = Pir(pir, led)
  
  def setup(self, led): #set up of the sensor to initialize
    GPIO.output(led, GPIO.LOW)
    print ("Sensor initializing . . .")
    #time.sleep(30) #Give sensor time to startup
    print ("50% . . .")
    time.sleep(10) #Give sensor time to startup
    print ("Active")
    print ("Press Ctrl+c to end program")
    GPIO.output(led, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(led, GPIO.LOW)  
  
  def runAlarm(self, pir, led): #runs the actual alarm
    stepper = Motor(pins)
    try:
      while True:
        if GPIO.input(pir) == True: #If PIR pin goes high, motion is detected
          print ("Motion Detected!")
          buzzer(13) #turn on buzzer to signal motion
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

def createAlarm(pir, led): #create a function to create and run alarm for multiprocessing
  security = Alarm(pir,led)
  security.setup(led)
  security.runAlarm(pir, led)

pir = 23 #Assign pin 8 to PIR
led = 21 #Assign pin 10 to LED
#run functions continuously with multiprocessing
motorcont = multiprocessing.Process(target=runMotor) 
motorcont.start() 
alarmset = multiprocessing.Process(target=createAlarm, args=(pir,led))
alarmset.start()