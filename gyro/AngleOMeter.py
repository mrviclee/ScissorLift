#Connections
#MPU6050 - Raspberry pi
#VCC - 5V  (2 or 4 Board)
#GND - GND (6 - Board)
#SCL - SCL (5 - Board)
#SDA - SDA (3 - Board)

import time

from AngleMeterAlpha import AngleMeterAlpha

angleMeter = AngleMeterAlpha()
angleMeter.measure()

while True:
    print(angleMeter.get_kalman_roll(),",", angleMeter.get_complementary_roll(), ",",angleMeter.get_kalman_pitch(),",", angleMeter.get_complementary_pitch(),".")
    #print(angleMeter.get_int_roll(), angleMeter.get_int_pitch())
    if (abs(angleMeter.get_int_roll()) > 30):
        print(f"Roll is uneven: { angleMeter.get_int_roll() }")
    if (abs(angleMeter.get_int_pitch()) > 30):
        print(f"Pitch is uneven: { angleMeter.get_int_pitch()} ")
    time.sleep(1)
    

