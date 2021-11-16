import RPi.GPIO as GPIO
from lx16a import *
import signal
import socket
import sys
from time import sleep

# This is the port that the controller board is connected to
# This will be different for different computers
# On Windows, try the ports COM1, COM2, COM3, etc...
# On Raspbian, try each port in /dev/
LX16A.initialize('/dev/ttyUSB0')
servo1 = LX16A(1)

# This setups the GPIO for the two limit switches
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)  #Down Stop
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)  #Up Stop

def shutdown(sig, frame):
    servo1.motorMode(0)
    print("quiting")
    exit(1)

signal.signal(signal.SIGINT, shutdown)

def wait_check_socket(conn):
    # print("reading.")
    sleep(.1) #Why do we need this?
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

def move_up(servo, UpperLimit, conn=None):
    #Move the slider to raise the scissor
    while UpperLimit == 'No':
        servo.motorMode(1000)
        if GPIO.input(22) == False:
            UpperLimit = 'Yes'
            servo.motorMode(0)
        # print ('going up')

def move_down(servo, LowerLimit, conn=None):
    #Move Slider to lower the scissor
    while LowerLimit == 'No':
        servo.motorMode(-1000)
        if GPIO.input(23) == False:
            LowerLimit = 'Yes'
            servo.motorMode(0)
        # print ('going down')
        
if __name__ == "__main__":
    # This sets the switch check to No and turnes off the motor
    LowerLimit = 'No'
    UpperLimit = 'No'
    servo1.motorMode(0)

    port = int(sys.argv[1]) if len(sys.argv) >= 2 else 5000

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(f"Listing on port {port}.")
    s.bind(("0.0.0.0", port))
    s.listen(5)
    conn, address = s.accept()
    conn.setblocking(0)

    # input("Press enter to start.")

    #Check to see if the slider is at either end.
    if GPIO.input(23) == False:
            LowerLimit = 'Yes'

    if GPIO.input(22) == False:
            UpperLimit = 'Yes'
    
    while True:
        move_up(servo1, UpperLimit, conn)
        # move_up(servo1, UpperLimit)
        LowerLimit = 'No'
        move_down(servo1, LowerLimit, conn)
        # move_down(servo1, LowerLimit)
        UpperLimit = 'No'
        

print ('done moving')
