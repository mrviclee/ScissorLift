#Connections
#MPU6050 - Raspberry pi
#VCC - 5V  (2 or 4 Board)
#GND - GND (6 - Board)
#SCL - SCL (5 - Board)
#SDA - SDA (3 - Board)

import time

if __debug__:
    from .AngleMeterAlpha import AngleMeterAlpha

# TODO: reduce time to measure GYRO

def get_gyro():
    angleMeter = AngleMeterAlpha()
    angleMeter.measure()
    
    time.sleep(.2)
    
    roll = angleMeter.get_int_roll()
    pitch = angleMeter.get_int_pitch()
    return {
        "roll" : roll,
        "pitch" : pitch
    }

def isLevel():
    if not __debug__:
        return True
    roll = get_gyro()["roll"]
    pitch = get_gyro()["pitch"]

    return roll < 15 and pitch < 15
