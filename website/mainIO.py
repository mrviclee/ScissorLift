from threading import Lock
from flask import Flask, render_template, request, flash
from flask_socketio import SocketIO, emit
import subprocess

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


async_mode = None
socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()

def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        socketio.sleep(10)
        count += 1
        socketio.emit('my_response',
                      {'data': 'Server generated event', 'count': count})

def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        socketio.sleep(10)
        count += 1
        socketio.emit('my_response',
                      {'data': 'Server generated event', 'count': count})

def not_level():
    flash("Drone valley is not within safe angle for take off.")

def error_opening():
    flash("Drone valley could not open lid.")

def not_open():
    flash("Drone valley could not open lid.")

def error_lifting():
    flash("Drone valley could not extend lift.")
    
def error_lowering():
    flash("Drone valley could not lower lift.")

def undifined():
    flash("Unknown error uccored.")

error_map = {
    1 : not_level,
    2 : error_opening,
    3 : not_open,
    4 : error_lifting,
    5 : error_lowering,
    255: undifined
}

@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("home.html", result = {'phy':50,'che':60,'maths':70})


def move_lid(instruction):
    ret = subprocess.call(f"./client {instruction}", shell=True)
    if (ret != 0):
        if ret not in error_map:
            ret = 255
        error_map[ret]()

@app.route("/open.html", methods=["GET", "POST"])
def open():
    move_lid("open")
    return render_template("home.html")

@app.route("/close.html", methods=["GET", "POST"])
def close():
    move_lid("close")
    return render_template("home.html", result = {'phy':50,'che':60,'maths':70})


@socketio.event
def my_ping():
    emit('my_pong')

@socketio.event
def connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_thread)
    emit('my_response', {'data': 'Connected', 'count': 0})

@socketio.on('connect')
def ws_connect():
    emit('my_response', {'data': 1})
    print('Client disconnected', request.sid)

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected', request.sid)

@socketio.on("message")
def recv_message():
    print("Recv:")

if __name__ == '__main__':
    socketio.run(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)