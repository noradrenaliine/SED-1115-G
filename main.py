#import needed libraries and functions
from machine import PWM, ADC, Pin
import math
import time
#function definitions:

def translate(angle:float) -> int: #translates an angle into a PWM output
   #The function checks if the input angle is between 0 and 180 degrees .
   if 0<= angle <= 180:
        #Calculates the PWM output using a linear interpolation formula
        #PWM is turned into 16-bit range (0 to 65535) and returned
        pwm_out = int((500 + (2000) * (angle / 180))*65535/20000)
    
    #angle is greater than 180 degrees,  default PWM output of 8192 
   elif angle > 180:
        pwm_out = 8192
    
    #angle is less than 0 degrees,  default PWM output of 1638
    else:
        pwm_out = 1638
    return pwm_out



def get_angles (cx,cy): #calculates brachiograph shoulder and elbow angles given x/y coordinates
#fixed servo positions on grid     
    ax = -50
    ay = 139.5
    la = 155
    lb = 155

    ac = math.sqrt( ((ax - cx)**2) + ((ay - cy)**2) )
    abase_c = math.sqrt(((ax - cx)**2) + cy**2)
    Abac = math.acos((la**2 + ac**2 - lb**2) / (2 * la * ac))  
    Aacb = math.asin((la * math.sin(Abac) / (lb)))
    Ayac = math.acos((ay**2 + ac**2 - abase_c**2) / (2*ay*ac))

#interpreting analog values to something the servos can use
    alpha = math.degrees(Abac + Ayac)
    beta = math.degrees(Abac + Aacb)

#ensures pen stays on plane     
    servoA = alpha - 75
    servoB = 150 - beta 
    
    return (servoA,servoB)

def move_servos(shoulderangle, elbowangle): #sends
    
    MIN_ANGLE_DEGREES = 0  # Minimum servo angle in degrees
    MAX_ANGLE_DEGREES = 180  # Maximum servo angle in degrees
    MIN_DUTY_CYCLE = 1000  # Minimum PWM duty cycle value for the servo
    MAX_DUTY_CYCLE = 2000  # Maximum PWM duty cycle value for the servo
    
    #process shoulder servo
    shoulderduty_cycle = translate(shoulderangle)
    
    #process elbow servo
    elbowduty_cycle = translate(elbowangle)
        
    #print("Shoulder duty cycle is:",shoulderduty_cycle, "Elbow duty cycle is:", elbowduty_cycle, end='\r')
    
    #move the servos to the req'd places
    shoulder.duty_u16(shoulderduty_cycle)
    elbow.duty_u16(elbowduty_cycle)
    
    return shoulderduty_cycle, elbowduty_cycle #return in case the duty cycles are needed elsewhere


def convert_potentiometer_to_x(degreeX):

    convertX = x_max/65535 #ratio by which the pot. value neeeds to be multiplied by to get a coordinate
    xval = convertX * degreeX
    #print ("X Coordinate:" + str(xval), end = '\r')

    return xval

def convert_potentiometer_to_y(degreeY):
    convertY = y_max/65535 #ratio by which the pot. value neeeds to be multiplied by to get a coordinate
    yval = y_max - convertY * degreeY
    #print ("                             Y Coordinate:" + str(yval), end = '\r')

    return yval

#combines the x and y convert functions and uses the readings from the potentiometers to return 
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


#initialize pwm and other pins
shoulder_pin = Pin(0)
elbow_pin = Pin(1)
wrist_pin = Pin(2)
piny = ADC(27)
pinx = ADC(26)
shoulder = PWM(shoulder_pin)
elbow = PWM(elbow_pin)
wrist = PWM(wrist_pin)
shoulder.freq(50)
elbow.freq(50)
wrist.freq(50)
button = Pin("GP22",Pin.IN)

#initialize variables
x_min = 40 #minimum writable x coordinate
y_min = 40 #minimum writable y coordinate
x_max = 200 #maximum writable x coordinate
y_max = 215 #maximum writable y coordinate

smooththreshold = 10 #minimum difference in mm between 2 sequential coordinate readings needed to activate smoothing
smoothamount = 7 #how many millimeters the arm limits itself to moving in each dimension when smoothing is active

wrist_down = translate(12) #position in degrees for the wrist servo to move the pencil into contact w paper
wrist_up = translate(0) #position in degrees for the wrist servo to lift the pencil off the paper

#move the wrist up in case it isn't already before moving things around
wrist.duty_u16(wrist_up)
wristDown = False

#get an initial reading of where the potentiometers are
values = read_potentiometer()
x_val = values[0]
y_val = values[1]

#the try here is not part of a try/except but a try/finally
#so that the servos deinitialize when the 
#program is stopped.
 
try: 
    while True: #loops forever :)
        old_x = x_val
        old_y = y_val
        values = read_potentiometer()
        x_val = values[0]
        y_val = values[1]
        
        #smooth the movement if a big jump is requested
        if abs(x_val-old_x)>smooththreshold:
            if x_val>old_x:
                x_val = old_x + smoothamount
            elif old_x>x_val:
                x_val = old_x - smoothamount
            time.sleep_ms(20)
        if abs(y_val-old_y)>smooththreshold:
            if y_val>old_y:
                y_val = old_y + smoothamount
            elif old_y>y_val:
                y_val = old_y - smoothamount
            time.sleep_ms(20)
        
        angles = get_angles(x_val, y_val)
        shoulder_angle = angles[0]
        elbow_angle = angles[1]
        time.sleep_ms(20)
        
        move_servos(shoulder_angle, elbow_angle)
        if (button.value() == 1): #if the button is pressed, this triggers and activates the
                                    #while not wristDown: loop.
            while (button.value() != 0):
                pass
                #do nothing while you wait for the button to be un-pressed
            if wristDown:
                wrist.duty_u16(wrist_up)
                wristDown = False #now the button is un-pressed and so it flips the boolean the other way to activate the other loop
            else:
                wrist.duty_u16(wrist_down)
                wristDown = True
        
finally: #deinitialize the servos so that they don't get damaged after the program is done running
    shoulder.deinit()
    elbow.deinit()
    wrist.deinit()
