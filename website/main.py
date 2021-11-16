from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("home.html", result = {'phy':50,'che':60,'maths':70})

@app.route("/open.html", methods=["GET", "POST"])
def open():
    print("run code to open box")
    return render_template("home.html")

@app.route("/close.html", methods=["GET", "POST"])
def close():
    print("write code to close box")
    return render_template("home.html", result = {'phy':50,'che':60,'maths':70})

if __name__ == "__main__":
    app.run(debug=True)
