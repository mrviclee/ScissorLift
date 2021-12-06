from asyncio.tasks import ensure_future
from types import coroutine
from lift.main import cleanup, move_up, move_down, yeet, cleanup, checkIR
from lift.main import servo1
from lift.main import servo2
from gyro.getGyroTest import get_gyro, isLevel
import time
import sys
from time import sleep
import asyncio
import websockets
import json
import threading
import signal
import os

def shutdown(sig, frame):
    cleanup()
    kill_thread = True
    print("quiting")
    os.kill(os.getpid(), signal.SIGUSR1)
    exit(1)

signal.signal(signal.SIGINT, shutdown)
g_moveTime = 0
if not __debug__:
    g_maxTime = 3000 
else:
    g_maxTime = 150000

def get_direction_from(func): #only returns "down" or "up"
    if "down" in func.__name__:
        return "down"
    elif "up" in func.__name__:
        return "up"
    else:
        return RuntimeError(f"Invalid fucntion name {func.__name__}")

def move(func, timeout):
    global g_moveTime
    timeout = int(timeout)
    dir = get_direction_from(func)
    print("direction is", dir)

    limit = "No"
    if __debug__:
        limit = func(servo1, limit, timeout)
    else:
        if g_moveTime >= g_maxTime and dir == "up":
            limit = "Success"
        elif g_moveTime <= 0 and dir == "down":
            limit = "Success"
        else:
            sleep(timeout / 1000)
            limit = "Failed:timeout"
    code = limit.split(":")[0]
    if code != "Success":
        if dir == "up":
            g_moveTime += timeout
        else:
            g_moveTime -= timeout
        return limit.split(":")[1]
    if dir == "down":
        g_moveTime = 0
    else:
        g_moveTime = g_maxTime
    return True

def lift(timeout="1000"):
    return move(move_up, timeout)

def lower(timeout="1000"):
    return move(move_down, timeout)

def open_lid(durration=1000):
    yeet(servo2, int(durration), -1)
    return True

def close_lid(durration=1000):
    yeet(servo2, int(durration), 1)
    return True

def close_box():
    print("Closing box")
    # Lower the scissor.
    move_down(servo1, 'No')

def is_open():
    sleep(.5)
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

def get_height():
    print("Movetime:", g_moveTime)
    if g_moveTime >= g_maxTime:
        return -1 #-1 denotes that we are at the top.
    return g_moveTime

function_map = {
        "hello" : get_hello,
        "lift" : lift,
        "close" : close_box,
        "is_level" : isLevel,
        "is_open" : is_open,
        "open" : open_lid,
        "" : do_nothing,
        "lower" : lower,
        "get_gyro" : get_gyro,
        "close": close_lid,
        "get_height" : get_height,
    }

async def handle_connection(conn):
    print("Handle connection is running...")
    while(True):
        try:
            msg = await conn.recv()
        except websockets.exceptions.ConnectionClosedError:
            break

        msg = msg.strip()
        print(f" <-- {msg}")

        try:
            data = json.loads(msg)
        except json.decoder.JSONDecodeError as e:
            print("ERROR: ", e)
            data = {
                "cmd" : msg
            }
        if type(data) == str:
            continue
        cmd = data.get("cmd")
        reply = ""
        data_type = ""
        if (cmd in function_map):
            try:
                if data.get("params"):
                    reply = function_map[cmd](*data.get("params"))
                else:
                    reply = function_map[cmd]()
                data_type = "success"
            except Exception as e:
                print("ERROR:", e)
                print("Cleaning up motors")
                cleanup()
                reply = str(e)
                data_type = "error"
        else:
            print("WARNING: invalid command:", msg)
            reply = f"invalid command: {cmd}"
            data_type = "invalid"

        msg = data.get("message")

        response = {
            "type" : data_type,
            "return" : reply,
            "message" : msg
        }

        to_send = json.dumps(response)
        await conn.send(to_send)
        print(f" --> {to_send}")

def between_callback(conn):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    loop.run_until_complete(handle_connection(conn))
    loop.close()

async def handler(conn, path):
    # t = threading.Thread(target=between_callback, args=(conn, ))
    t = threading.Thread(target=asyncio.run, args=(handle_connection(conn),))
    t.start()
    t.join()
    # await asyncio.wait([handle_connection(uri) for uri in connections])

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) >= 2 else 5050

    print(f"Listing on port {port}.")
    # start_server = websockets.serve(handler, '0.0.0.0', port)
    start_server = websockets.serve(handle_connection, '0.0.0.0', port)
    # start_server1 = websockets.serve(handle_connection, '0.0.0.0', port + 1)
    # start_server2 = websockets.serve(handle_connection, '0.0.0.0', port + 2)

    asyncio.get_event_loop().run_until_complete(start_server)
    # asyncio.get_event_loop().run_until_complete(start_server1)
    # asyncio.get_event_loop().run_until_complete(start_server2)
    asyncio.get_event_loop().run_forever()
