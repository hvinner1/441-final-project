import RPi.GPIO as GPIO
import time
from pir import Pir
from motor import Motor
from keyclass import Keypad
GPIO.setmode(GPIO.BCM)
import multiprocessing
import json

global pins, cw, ccw, state
state= "Arm Alarm"
pins = [18,20,22,24] # controller inputs: in1, in2, in3, in4
ccw = [ [1,0,0,0],[1,1,0,0],[0,1,0,0],[0,1,1,0],
        [0,0,1,0],[0,0,1,1],[0,0,0,1],[1,0,0,1] ]
cw = ccw[:]  # use slicing to copy list 
cw.reverse()

def runMotor():
  stepper = Motor(pins)
  try:
    while True:
      stepper.loop(cw)
      stepper.loop(ccw)
  except e:
    print(e)
    pass

  GPIO.cleanup()

def buzzer(BUZZER):
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
  
def checkHTML():
  with open('pinData.txt', 'r') as pinDataRead:
            pinData = json.load(pinDataRead)
            state = pinData['selection']
            secretCode = pinData['pin']
            # Three different possible states
            # 'Turn Off Alarm' -> disables alarm
            # 'Arm Alarm' -> sensing
            # 'Reset Pin' -> changes pin
def updateHTML(state):
  dataDump = {'pin':secretCode,'selection':state}
  with open('pinData.txt', 'w') as f:
    json.dump(dataDump, f)
            # Three different possible states
            # 'Turn Off Alarm' -> disables alarm
            # 'Arm Alarm' -> sensing
            # 'Reset Pin' -> changes pin



class Alarm():

  def __init__(self, pir, led):
    self.alarm = Pir(pir, led)
  
  def setup(self, led):
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
    state = 'Arm Alarm'
  
  def runAlarm(self, pir, led):
    stepper = Motor(pins)
    try:
      while True:
        if GPIO.input(pir) == True: #If PIR pin goes high, motion is detected
          print ("Motion Detected!")
          state = 'beeping'
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

def createAlarm(pir, led):
  security = Alarm(pir,led)
  security.setup(led)
  security.runAlarm(pir, led)

L1 = 4
L2 = 27
L3 = 17
L4 = 5
C1 = 6
C2 = 19
C3 = 26
C4 = 16
keypadPressed = -1
pir = 23 #Assign pin 8 to PIR
led = 21 #Assign pin 10 to LED
key = Keypad(L1, L2, L3, L4, C1, C2, C3, C4)
htmlchecker = multiprocessing.Process(target=checkHTML)
htmlchecker.start()
motorcont = multiprocessing.Process(target=runMotor) 
motorcont.start()
alarmset = multiprocessing.Process(target=createAlarm, args=(pir,led))
alarmset.start()


while state == 'Arm Alarm':
  motorcont = multiprocessing.Process(target=runMotor) 
  motorcont.start()
  alarmset = multiprocessing.Process(target=createAlarm, args=(pir,led))
  alarmset.start()
  state = 'beeping'
  updateHTML(state)
while state == 'beeping':
  keyOn = multiprocessing.Process(target=Keypad)
  keyOn.start()
  if secretCode == input:
    state = 'Turn Off Alarm'
    updateHTML(state)
while state == 'Turn Off Alarm':
  off motors
  until html says armed
  #state = 'Arm Alarm'
