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
    subprocess.call(["client", "open"])

if __name__ == "__main__":
    app.run(debug=True)
    # open()