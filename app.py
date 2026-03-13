from flask import Flask, render_template, request, redirect, url_for
from register import register_student
from camera import start_camera

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/register")
def register_page():
    return render_template("register.html")


@app.route("/register_student", methods=["POST"])
def register():

    name = request.form["name"]
    roll = request.form["roll"]

    register_student(name, roll)

    return redirect(url_for("home"))


@app.route("/attendance")
def attendance():
    start_camera()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)