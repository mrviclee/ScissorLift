from flask import Flask, render_template, request, flash
import subprocess

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


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
    open()
    if request.method == "POST":
        print("Post")
    else:
        print("Hello")
    return render_template("test.html")

def open():
    ret = subprocess.call("./client", shell=True)
    if (ret != 0):
        if ret not in error_map:
            ret = 255
        error_map[ret]()

def close():
    ret = subprocess.call("./client close", shell=True)
    if (ret != 0):
        if ret not in error_map:
            ret = 255
        error_map[ret]()

if __name__ == "__main__":
    app.run(debug=True)