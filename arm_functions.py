from machine import Pin
from machine import PWM
from machine import ADC

#config pins
shoulder_pin = PWM(Pin(0))
elbow_pin = PWM(Pin(1))
x_knob_uni = ADC(26)
y_knob_uni = ADC(27)
#initialize paper dimensions in millimetres
x_max = 210
y_max = 275
#resolution in mm of drawing
resolution = 5
#set freq for shoulder and elbow
shoulder_pin.freq(50)
elbow_pin.freq(50)

#replace these with the actual initial values given the math
shoulder_angle = 0
elbow_angle = 0

def translate(angle:float) -> int:
    if 0<= angle <= 180:
        pwm_out = int((500 + (2000) * (angle / 180))*65535/20000)
    elif angle > 180:
        pwm_out = 8192
    else:
        pwm_out = 1638
    return pwm_out

def move_shoulder(angle:float, shoulder:PWM = shoulder_pin,):
    pwm_out = translate(angle)
    shoulder.duty_u16(pwm_out)

def move_elbow( angle:float, elbow:PWM = shoulder_pin):
    pwm_out = translate(angle)
    elbow.duty_u16(pwm_out)

def get_x_mm(knob:ADC = x_knob_uni):
    read_analog = knob.read_u16()
    millimetre_value = ((read_analog/65535)*x_max)
    return millimetre_value

def get_y_mm(knob:ADC = y_knob_uni):
    read_analog = knob.read_u16()
    millimetre_value = (y_max - ((read_analog/65535)*y_max))
    return millimetre_value


def calculate_shoulder(angle = 0, change_in_x = 0, change_in_y = 0) -> int:
    angle += change_in_x + change_in_y #add the actual math here
    return angle

def calculate_elbow(angle = 0, change_in_x = 0,change_in_y = 0) -> int:
    angle += change_in_x + change_in_y #add the actual math here
    return angle

def update_arm(knob_x:ADC = x_knob_uni, knob_y:ADC = y_knob_uni, original_x = get_x_mm(), original_y = get_y_mm()):
    change_in_x = False
    change_in_y = False
    new_x = get_x_mm(knob_x)
    new_y = get_x_mm(knob_y)
    if abs(new_x-original_x) >= resolution:
        x_change = new_x-original_x
        change_in_x = True
    else:
        x_change = 0
    if abs(new_y-original_y) >= resolution:
        y_change = new_y-original_y
        change_in_y = True
    else:
        y_change = 0
    if change_in_x or change_in_y:
        #calculate the angle each servo has to move
        try: shoulder_angle = calculate_shoulder(shoulder_angle, change_in_x,change_in_y)
        except:
            shoulder_angle = 0
            shoulder_angle = calculate_shoulder(shoulder_angle, change_in_x,change_in_y)
        elbow_angle = calculate_elbow(elbow_angle, change_in_x, change_in_y)
        #move the servos
        move_shoulder(shoulder_angle)
        move_elbow(elbow_angle)
    original_x = new_x
    original_y = new_y