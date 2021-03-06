
"""
put max pitch and roll - green is good red it not good orange is not good



Better state displaying (opening, closing, ready to launch, error, stopped)

Do dumb user testing
Test on phone
Fix progress bar.  Progress bar should go up

"""

from threading import Lock
from flask import Flask, render_template, request, flash
# from flask_socketio import SocketIO, emit
import subprocess

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# socketio = SocketIO(app)

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
    return render_template("home.html")

def move_lid(instruction):
    ret = subprocess.call(f"./client {instruction}", shell=True)
    if (ret != 0):
        if ret not in error_map:
            ret = 255
        error_map[ret]()

# @socketio.on('connect')
# def ws_connect():
#     print("Cliented connected.")

# @socketio.on('disconnect')
# def test_disconnect():
#     print("Client disconnected.")

# @socketio.on("message")
# def recv_message():
#     print("Recv:")

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
    # socketio.run(app)
