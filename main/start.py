import subprocess
import signal
import sys
from time import sleep

def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    sys.exit(0)

# signal.signal(signal.SIGINT, signal_handler)

if __name__ == "__main__":
    start_port = 5050
    childs = []
    for i in range(3):
        childs.append(subprocess.Popen(f"python main.py {start_port + i}", shell=True))
        sleep(1)
    
    for p in childs:
        p.wait()