#import needed libraries and functions
from machine import PWM, ADC, Pin
#from armfuncs import angles_to_duty_cycles as move_servos
#from IK import get_angles
import math
import time
import random
def translate(angle:float) -> int:
    if 0<= angle <= 180:
        pwm_out = int((500 + (2000) * (angle / 180))*65535/20000)
    elif angle > 180:
        pwm_out = 8192
    else:
        pwm_out = 1638
    return pwm_out

def get_angles (cx,cy):
    
    ax = -50
    ay = 139.5
    la = 155
    lb = 155

    ac = math.sqrt( ((ax - cx)**2) + ((ay - cy)**2) )
    abase_c = math.sqrt(((ax - cx)**2) + cy**2)
    Abac = math.acos((la**2 + ac**2 - lb**2) / (2 * la * ac))  
    Aacb = math.asin((la * math.sin(Abac) / (lb)))
    Ayac = math.acos((ay**2 + ac**2 - abase_c**2) / (2*ay*ac))

    alpha = math.degrees(Abac + Ayac)
    beta = math.degrees(Abac + Aacb)
    
    servoA = alpha - 75
    servoB = 150 - beta 
    
    return (servoA,servoB)

def move_servos(shoulderangle, elbowangle):
    
    MIN_ANGLE_DEGREES = 0  # Minimum servo angle in degrees
    MAX_ANGLE_DEGREES = 180  # Maximum servo angle in degrees
    MIN_DUTY_CYCLE = 1000  # Minimum PWM duty cycle value for the servo
    MAX_DUTY_CYCLE = 2000  # Maximum PWM duty cycle value for the servo
    
    #process shoulder servo
    if 0<= shoulderangle <= 180:
        shoulderduty_cycle = int((500 + (2000) * (shoulderangle / 180))*65535/20000)

    elif shoulderangle > 180:
        shoulderduty_cycle = 8192
    else:
        shoulderduty_cycle = 1638
    
    #process elbow servo
    if 0<= elbowangle <= 180:
        elbowduty_cycle = int((500 + (2000) * (elbowangle / 180))*65535/20000)

    elif elbowangle > 180:
        elbowduty_cycle = 8192
    else:
        elbowduty_cycle = 1638
        
    print("Shoulder duty cycle is:",shoulderduty_cycle, "Elbow duty cycle is:", elbowduty_cycle, end='\r')
        
    shoulder.duty_u16(shoulderduty_cycle)
    elbow.duty_u16(elbowduty_cycle)
    return shoulderduty_cycle, elbowduty_cycle


#initialize pwm 
shoulder_pin = 0
elbow_pin = 1
wrist_pin = 2
shoulder = PWM(Pin(shoulder_pin))
elbow = PWM(Pin(elbow_pin))
wrist = PWM(Pin(wrist_pin))
shoulder.freq(50)
elbow.freq(50)
wrist.freq(50)

#initialize variables
x_min = 50
y_min = 30
x_max = 120
y_max = 150
x_knob_uni = ADC(26)
y_knob_uni = ADC(27)

#set freq for shoulder and elbow
shoulder.freq(50)
elbow.freq(50)
#record initial pot. positions
#x_old = x.get()
#y_old = y.get()

#calculate starting angles for 0,0 x,y
x_val = x_min
y_val = y_min
x_increasing = True
y_increasing = True
mod_value = 1
wrist_down = translate(20)
wrist.duty_u16(wrist_down)
try:
    while True:
        if x_increasing:
            x_val += mod_value
        else:
            x_val -= mod_value
        if y_increasing:
            y_val += mod_value
        else:
            y_val -= mod_value
        angles = get_angles(x_val, y_val)
        shoulder_angle = angles[0]
        elbow_angle = angles[1]
        angles = get_angles(x_val, y_val)
        shoulder_angle = angles[0]
        elbow_angle = angles[1]

        move_servos(shoulder_angle, elbow_angle)
        if x_val >= x_max:
            x_increasing = False
        if x_val <= x_min:
            x_increasing = True
        if y_val >= y_max:
            y_increasing = False
        if y_val <= y_min:
            y_increasing = True
        mod_value = 1+3*(random.random())
        time.sleep_us(3000*(int(mod_value)))
finally:
    shoulder.deinit()
    elbow.deinit()
    wrist.deinit()

#while True:
    #record new pot. values

    #x_new = x.get()
    #y_new = y.get()

    #calculate changes in each dimension

    #x_difference = x_new - x_old
    #y_difference = y_new - y_old

    #convert the changes in each dimension to angles

    #move_servos(shoulder_angle, elbow_angle)
