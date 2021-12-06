import subprocess
import signal
import sys
from time import sleep

def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    sys.exit(0)

# signal.signal(signal.SIGINT, signal_handler)

if __name__ == "__main__":
    start_port = 6050
    childs = []
    mode = "-O" if not __debug__ else ""
    for i in range(3):
        cmd = f"python {mode} main.py {start_port + i}" 
        #print(f"cmd: {cmd}")
        childs.append(subprocess.Popen(cmd, shell=True))
        sleep(1)
    
    for p in childs:
        p.wait()
