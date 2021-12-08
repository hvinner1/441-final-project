import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

pins = [18,20,22,24] # controller inputs: in1, in2, in3, in4
for pin in pins:
  GPIO.setup(pin, GPIO.OUT, initial=0)

# Define the pin sequence for counter-clockwise motion, noting that
# two adjacent phases must be actuated together before stepping to
# a new phase so that the rotor is pulled in the right direction:
ccw = [ [1,0,0,0],[1,1,0,0],[0,1,0,0],[0,1,1,0],
        [0,0,1,0],[0,0,1,1],[0,0,0,1],[1,0,0,1] ]
# Make a copy of the ccw sequence. This is needed since simply
# saying cw = ccw would point both variables to the same list object:
cw = ccw[:]  # use slicing to copy list (could also use ccw.copy() in Python 3)
cw.reverse() # reverse the new cw sequence

def delay_us(tus): # use microseconds to improve time resolution
  endTime = time.time() + float(tus)/ float(1E6)
  while time.time() < endTime:
    pass

# Make a full rotation of the output shaft:
def loop(dir): # dir = rotation direction (cw or ccw)
  for i in range(512): # full revolution (8 cycles/rotation * 64 gear ratio)
    for halfstep in range(8): # 8 half-steps per cycle
      for pin in range(4):    # 4 pins that need to be energized
        GPIO.output(pins[pin], dir[halfstep][pin])
      delay_us(1000)
try:
  while True:
    loop(cw)
    loop(ccw)
except:
  pass
  GPIO.cleanup() 

