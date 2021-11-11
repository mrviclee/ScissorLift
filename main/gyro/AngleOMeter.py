#Connections
#MPU6050 - Raspberry pi
#VCC - 5V  (2 or 4 Board)
#GND - GND (6 - Board)
#SCL - SCL (5 - Board)
#SDA - SDA (3 - Board)

import time

from .AngleMeterAlpha import AngleMeterAlpha


def isLevel():
    angleMeter = AngleMeterAlpha()
    angleMeter.measure()
    time.sleep(2)

    roll = abs(angleMeter.get_int_roll())
    pitch = abs(angleMeter.get_int_pitch())

    angleMeter.angleThread.join
    return roll < 30 and pitch < 30
