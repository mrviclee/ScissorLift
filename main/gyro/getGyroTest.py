# from gyroMonitor import * #g_roll
from . import gyroMonitor

# Usage: python3 getGyroTest.py 
# todo: implement isLevel() functionality to server/client communications for physical operation.

import time
def get_gyro():
    pitch = gyroMonitor.g_pitch
    roll = gyroMonitor.g_roll
    #pitch = q_pitch.get()
    #roll = q_roll.get()
    time.sleep(.5)
    
    return {
        "roll" : roll, "pitch" : pitch
    }

def isLevel():
    if not __debug__:
        return True
    roll = get_gyro()["roll"]
    pitch = get_gyro()["pitch"]
    return roll < 15 and pitch < 15

def main():
    time.sleep(.5)
    while True:
        print ("getGyroTest: isLevel " + str(isLevel()) + "\npitch: " + str(get_gyro()["pitch"]) + "\nroll:"+ str(get_gyro()["roll"]) )
        time.sleep(.4)

if __name__ == "__main__":
    main()

# if KeyboardInterrupt:
#     gyroMonitor.kill_thread = True
#     gyroMonitor.t.join()
