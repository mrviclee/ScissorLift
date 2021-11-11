# from lift.main import move_up
from gyro.AngleOMeter import isLevel
import time

def open_box():
    print("Opening box")

def is_go():
    user_input = input("Enter command...\n")
    return user_input == "go"

if __name__ == "__main__":
    while(True):
        if (is_go() and isLevel()):
            break
    open_box()
    exit(0)