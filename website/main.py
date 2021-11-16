from flask import Flask, render_template, request
import subprocess

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        print("Post")
    else:
        print("Hello")
    return render_template("home.html")

def open():
    ret = subprocess.check_output(["client"])
    print("Ret:", ret)

def open():
    subprocess.call(["client", "close"])

if __name__ == "__main__":
    # app.run(debug=True)
    open()