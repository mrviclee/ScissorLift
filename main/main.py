from asyncio.tasks import ensure_future
from types import coroutine
from lift.main import cleanup, move_up, move_down, yeet, cleanup, checkIR
from lift.main import servo1
from lift.main import servo2
# from gyro.AngleOMeter import get_gyro, isLevel
from gyro.getGyroTest import get_gyro, isLevel
from gyro.gyroMonitor import kill_thread
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
    sleep(.2)
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
        "lower" : lower,
        "get_gyro" : get_gyro,
        "close": close_lid,
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