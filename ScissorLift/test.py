import RPi.GPIO as GPIO
from lx16a import *

# This is the port that the controller board is connected to
# This will be different for different computers
# On Windows, try the ports COM1, COM2, COM3, etc...
# On Raspbian, try each port in /dev/
LX16A.initialize('/dev/ttyUSB0')
servo1 = LX16A(1)

# This setups the GPIO for the two limit switches
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(True)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)  #Down Stop
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)  #Up Stop

# This sets the switch check to No and turnes off the motor
servo1.motorMode(0)


#Check to see if the slider is at either end.

#Move the slider to raise the scissor
count = 0
while True:
    if count >= 10000:
        UpperLimit = 'Yes'
        servo1.motorMode(0)
        break
    servo1.motorMode(500)
    count+=1
    

# #Move Slider to lower the scissor
# while LowerLimit == 'No':
#     if GPIO.input(23) == False:
#         LowerLimit = 'Yes'
#         servo1.motorMode(0)
#     print ('going down')
#     servo1.motorMode(-1000)
#     UpperLimit = 'No'
# servo1.motorMode(0)

print ('done moving')
