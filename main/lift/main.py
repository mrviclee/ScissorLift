if __debug__:
    import RPi.GPIO as GPIO
    from .lx16a import *
else:
    from .fake_lx16a import *
import signal
import socket
import sys
import threading
import time
from datetime import datetime

# This is the port that the controller board is connected to
# This will be different for different computers
# On Windows, try the ports COM1, COM2, COM3, etc...
# On Raspbian, try each port in /dev/
LX16A.initialize('/dev/ttyUSB0')
servo1 = LX16A(1)
servo2 = LX16A(2)

# This setups the GPIO for the two limit switches
if __debug__:
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)  #Down Stop
    GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)  #Up Stop
    GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)  #IR Sensor, high = something blocking or not plugged in.


def cleanup():
    servo1.motorMode(0)
    servo2.motorMode(0)

def checkIR():
    return GPIO.input(26) == 1 # 1 Means no block, 0 means block

def wait_check_socket(conn):
    # print("reading.")
    time.sleep(.1) #Why do we need this?
    currentMode = servo1.servoMotorModeRead()
    msg = "nothing"

    try:
        msg = conn.recv(1024)
    except BlockingIOError:
        pass

    if (msg.strip() == b"stop"):
        servo1.motorMode(0)
        while msg.strip() != b"go":
            try:
                msg = conn.recv(1024)
            except BlockingIOError:
                pass
    print("Current mode:", currentMode)
    if (type(currentMode) == int):
        servo1.motorMode(currentMode)
    else:
        servo1.motorMode(currentMode[1])


def move_up(servo, UpperLimit, maxTime = -1, conn=None):
    start = datetime.now()
    while UpperLimit == 'No':
        servo.motorMode(1000)
        if GPIO.input(22) == False:
            UpperLimit = "Success:pressed"
        if (datetime.now() - start).total_seconds() * 1000 >= maxTime:
            UpperLimit = 'Failed:timeout'
    servo.motorMode(0)
    return UpperLimit

def move_down(servo, LowerLimit, maxTime = -1, conn=None):
    start = datetime.now()
    while LowerLimit == 'No':
        servo.motorMode(-1000)
        if GPIO.input(23) == False:
            LowerLimit = "Success:pressed"
        if (datetime.now() - start).total_seconds() * 1000 >= maxTime:
            LowerLimit = 'Failed:timeout'
    servo.motorMode(0)
    return LowerLimit

#def yeet(servo, degree, timer, conn=None):
def yeet(servo, timer, dir, conn=None):
    # Move it to that degree
    print("Yeeting")
    #servo.moveTimeWrite( degree, time)
    servo.motorMode(1000 * dir) #TODO: Switch to working with degrees.
    time.sleep(timer / 1000)
    servo.motorMode(0)
    print("Yeet complete")
        
if __name__ == "__main__":
    # This sets the switch check to No and turnes off the motor
    LowerLimit = 'No'
    UpperLimit = 'No'
    servo1.motorMode(0)

    input("Press enter to start.")

    #Check to see if the slider is at either end.
    if GPIO.input(23) == False:
            LowerLimit = 'Yes'

    if GPIO.input(22) == False:
            UpperLimit = 'Yes'
    
    while True:
        move_up(servo1, UpperLimit)
        LowerLimit = 'No'
        move_down(servo1, LowerLimit)
        UpperLimit = 'No'
        