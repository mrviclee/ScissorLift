from lift.main import move_up, move_down, yeet, servo1
from lift.main import servo2
from gyro.AngleOMeter import isLevel
import time

def open_box():
    print("Opening box")
    # Step 1: TODO: Yeet the thing
    time.sleep(1)
    yeet(servo2, 1.6)
    time.sleep(1)
    # Step 2: Lift the scissor.
    move_up(servo1, 'No')

def close_box():
    print("Closing box")
    # Lower the scissor.
    move_down(servo1, 'No')

def is_go():
    user_input = input("Enter command...\n")
    return user_input == "go"

if __name__ == "__main__":
    while(True):
        if (is_go() and isLevel()):
            break
    open_box()

    # Close the box later

    close_box()

    exit(0)
