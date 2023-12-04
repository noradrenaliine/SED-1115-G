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

def move_servos(shoulderangle, elbowangle, formershoulder, formerelbow):
    
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
    shoulder_send = formershoulder
    elbow_send = formerelbow
    #shoulder.duty_u16(shoulderduty_cycle)
    #elbow.duty_u16(elbowduty_cycle)
      
    shoulder.duty_u16(shoulder_send)
    elbow.duty_u16(elbow_send)
    
    return shoulderduty_cycle, elbowduty_cycle

def convert_potentiometer_to_x(degreeX):
    convertX = x_max/65535
    xval = convertX * degreeX
    print ("X Coordinate:" + str(xval), end = '\r')

    return xval

def convert_potentiometer_to_y(degreeY):
    convertY = y_max/65535
    yval = y_max - convertY * degreeY
    print ("                             Y Coordinate:" + str(yval), end = '\r')

    return yval
def read_potentiometer():
    while True:
        if pinx.read_u16() > 0:
            degreeX = pinx.read_u16()
            x_val = convert_potentiometer_to_x(degreeX)
            if x_val < x_min:
                x_val = x_min
            if x_val > x_max:
                x_val = x_max
        else: x_val = x_min
        if piny.read_u16() > 0:
            degreeY = piny.read_u16()
            y_val = convert_potentiometer_to_y(degreeY)
            if y_val < y_min:
                y_val = y_min
            if y_val > y_max:
                y_val = y_max
        else: y_val = y_min
        return x_val,y_val


#initialize pwm 
shoulder_pin = 0
elbow_pin = 1
wrist_pin = 2
piny = ADC(27)
pinx = ADC(26)
shoulder = PWM(Pin(shoulder_pin))
elbow = PWM(Pin(elbow_pin))
wrist = PWM(Pin(wrist_pin))
shoulder.freq(50)
elbow.freq(50)
wrist.freq(50)

#initialize variables
x_min = 20
y_min = 30
x_max = 200
y_max = 215
x_knob_uni = ADC(26)
y_knob_uni = ADC(27)
button = Pin("GP22",Pin.IN)
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
wrist_up = translate(0)
wrist.duty_u16(wrist_up)

angles = get_angles(x_val, y_val)
shoulder_angle = angles[0]
elbow_angle = angles[1]

old_values = move_servos(shoulder_angle, elbow_angle, 0, 0)
wrist.duty_u16(wrist_down)
wristDown = True

try:
    while True:
        while wristDown:
            
            values = read_potentiometer()
            x_val = values[0]
            y_val = values[1]
            angles = get_angles(x_val, y_val)
            shoulder_angle = angles[0]
            elbow_angle = angles[1]
            time.sleep_ms(20)
            
            old_values = move_servos(shoulder_angle, elbow_angle, old_values[0], old_values[1])
            if (button.value() == 1):
                while (button.value() != 0):
                    pass
                    #do nothing while you wait for the button to be un-pressed
                wristDown = False
        while not wristDown:
            wrist.duty_u16(wrist_up)
            if (button.value() == 1):
                while (button.value() != 0):
                    pass
                    #do nothing while you wait for the button to be un-pressed
                wristDown = True
                wrist.duty_u16(wrist_down)
        
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
