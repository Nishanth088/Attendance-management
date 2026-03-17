from flask import Flask, render_template, request
import pandas as pd
from register import capture_face
from camera import take_attendance, verify_face
import os

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


# ---------------- REGISTER ----------------
@app.route("/register", methods=["GET","POST"])
def register():

    if request.method == "POST":
        name = request.form["name"]
        roll = request.form["roll"]

        capture_face(name, roll)

        return "Face Registered Successfully"

    return render_template("register.html")


# ---------------- SUBJECT + ATTENDANCE ----------------
@app.route("/attendance", methods=["GET","POST"])
def attendance():

    if request.method == "POST":
        subject = request.form["subject"]
        take_attendance(subject)
        return "Attendance Completed"

    return render_template("subject.html")


# ---------------- CHECK PAGE ----------------
@app.route("/check")
def check():
    return render_template("check.html")


# ---------------- VERIFY ----------------
@app.route("/verify", methods=["POST"])
def verify():

    name = request.form["name"]
    roll = request.form["roll"]

    if verify_face(roll):

        if not os.path.exists("attendance.csv") or os.stat("attendance.csv").st_size == 0:
            df = pd.DataFrame(columns=["Name","Roll","Subject","Date","Time"])
            df.to_csv("attendance.csv", index=False)

        df = pd.read_csv("attendance.csv")

        if "Roll" not in df.columns:
            df.columns = ["Name","Roll","Subject","Date","Time"]

        student = df[df["Roll"].astype(str) == str(roll)]

        data = student.to_dict(orient="records")

        # 🔥 SUBJECT-WISE COUNT
        subject_count = student.groupby("Subject").size().to_dict()

        return render_template(
            "attendance_view.html",
            name=name,
            roll=roll,
            data=data,
            subject_count=subject_count
        )

    return "Face not matched"


if __name__ == "__main__":
    app.run(debug=True)