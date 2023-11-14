# SED-1115-G
#1. Initializing Rasberry Pi Pico
from machine import Pin
from machine import PWM
from machine import ADC

#Configure pins
shoulder = PWM (PIN(0))
elbow = PWN (Pin(1))
xknob = PWM ()     #pin on board
yknob = PWM ()     #pin on board
#Initialize dimensions of paper in mm
xmax = 220
ymax = 300

#Set frequency for shoulder and elbow
shoulder.freq ()
elbow.freq ()

#Set = 0, actual values
shoulder = 0
elbow = 0 
