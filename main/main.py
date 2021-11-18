from lift.main import cleanup, move_up, move_down, yeet, cleanup, checkIR
from lift.main import servo1
from lift.main import servo2
from gyro.AngleOMeter import isLevel
import time
import socket
import sys
from time import sleep
import asyncio
import websockets
import functools
import json

def move(func, timeout):
    timeout = int(timeout)
    print(f"Calling {func}.")
    limit = "No"
    limit = func(servo1, limit, timeout)
    code = limit.split(":")[0]
    if code != "Success":
        return limit.split(":")[1]
    return True

def lift(timeout="1000"):
    return move(move_up, timeout)

def lower(timeout="1000"):
    return move(move_down, timeout)

def open_lid():
    yeet(servo2, 1)
    return True

def close_box():
    print("Closing box")
    # Lower the scissor.
    move_down(servo1, 'No')

def is_open():
    return checkIR()

def is_go(conn=None):
    #conn.setblocking(0)
    user_input = conn.recv(1024)
    user_input = user_input.decode().strip()
    if (user_input == "go"):
        return True
    else:
        print("Received: ", user_input)

def get_hello(name="you"):
    return f"Hello to {name}."

def is_opepn():
    return False

def do_nothing():
    pass
    return ""

function_map = {
        "hello" : get_hello,
        "lift" : lift,
        "close" : close_box,
        "is_level" : isLevel,
        "is_open" : is_open,
        "open" : open_lid,
        "" : do_nothing,
        "lower" : lower
    }

async def handle_connection(conn):
     while(True):
        try:
            msg = await conn.recv()
        except websockets.exceptions.ConnectionClosedError:
            break

        msg = msg.strip()
        print(f" <-- {msg}")

        try:
            data = json.loads(msg) #TODO: accept invalid json
        except json.decoder.JSONDecodeError:
            data = {
                "cmd" : msg
            }
        cmd = data.get("cmd")
        reply = ""
        type = ""
        if (cmd in function_map):
            try:
                if data.get("params"):
                    reply = function_map[msg](*data.get("params"))
                else:
                    reply = function_map[msg]()
                type = "success"
            except Exception as e:
                print("ERROR:", e)
                print("Cleaning up motors")
                cleanup()
                reply = str(e)
                type = "error"
        else:
            print("WARNING: invalid command:", msg)
            reply = f"invalid command: {cmd}"
            type = "invalid"

        response = {
            "type" : type,
            "return" : reply
        }

        to_send = json.dumps(response)
        await conn.send(to_send)
        print(f" --> {to_send}")

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) >= 2 else 5050

    print(f"Listing on port {port}.")
    start_server = websockets.serve(handle_connection, '0.0.0.0', port)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()