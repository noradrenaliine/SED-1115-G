from machine import Pin, PWM
import time
servo = PWM(Pin(0))
servo.freq(50) 
            

# Initialize PWM controller
#pwm = PWM(0)

# Define pin assignments for servo motors
SERVO_PIN_1 = 0
SERVO_PIN_2 = 1

# Configure GPIO pins for servo control
#pwm.init(freq=50, s1=SERVO_PIN_1, s2=SERVO_PIN_2)
#Come back to frequency

# Initialize dimensions of paper in mm
shouldermax = 220
elbowmax = 300

# Set frequency for shoulder and elbow (assumed frequency is 50 Hz)
shoulder = PWM(Pin(0))  
elbow = PWM(Pin(1))  
shoulder.freq(50)
elbow.freq(50)
# Set initial angles to 0 (assuming 0 degrees is the default position)
shoulder.duty_u16(1638)
elbow.duty_u16(1638)

# Return the PWM controller for later use

        
# Function to Convert Angle to PWM Duty Cycle
def angles_to_duty_cycles(shoulderangle, elbowangle):
    
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
        
    print("Shoulder duty cycle is:",shoulderduty_cycle, "Elbow duty cycle is:", elbowduty_cycle)
        
    shoulder.duty_u16(shoulderduty_cycle)
    elbow.duty_u16(elbowduty_cycle)
    return shoulderduty_cycle, elbowduty_cycle


def translate(angle: float) -> int:
    """
    Converts an angle in degrees to the corresponding input
    for the duty_u16 method of the servo class

    See https://docs.micropython.org/en/latest/library/machine.PWM.html for more
    details on the duty_u16 method
    """

    MIN = 1638 # 0 degrees
    MAX = 8192 # 180 degrees
    DEG = (MAX - MIN) / 180 # value per degree

    # clamp angle to be between 0 and 180
    angle = max(0, min(180, angle))

    return int(angle * DEG + MIN)


def wrist (gcode_line, pen_switch_state):    
    
    if 'PEN_UP' in gcode_line:
        # Perform actions to lift the pen
        print("Lifting the pen") 
        servo.duty_u16(translate(0))
                  
            
    elif 'PEN_DOWN' in gcode_line:
        print("Lowering the pen")
        servo.duty_u16(translate(30))
                
                  
    else:
        # Handle other G-Code commands or ignore if not relevant
        print("Ignoring other G-Code commands")
        

angles_to_duty_cycles (0, 90)
time.sleep(3)
angles_to_duty_cycles (90, 90)
time.sleep(3)
angles_to_duty_cycles (45, 90)
time.sleep(3)
angles_to_duty_cycles (45, 45)


#Lifting and Lowering
