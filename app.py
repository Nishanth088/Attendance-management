from flask import Flask, render_template, request
import pandas as pd
import os
import calendar
from datetime import datetime

from camera import take_attendance, verify_face
from register import capture_face

app = Flask(__name__)


# -------------------------------
# HOME
# -------------------------------
@app.route("/")
def home():
    return render_template("index.html")


# -------------------------------
# REGISTER
# -------------------------------
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        roll = request.form["roll"]

        if not os.path.exists("students.csv") or os.stat("students.csv").st_size == 0:
            df = pd.DataFrame(columns=["Name", "Roll"])
            df.to_csv("students.csv", index=False)

        df = pd.read_csv("students.csv")

        new_row = {"Name": name, "Roll": roll}
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv("students.csv", index=False)

        capture_face(name, roll)

        return render_template("result.html", message="Student registered successfully")

    return render_template("register.html")


# -------------------------------
# ATTENDANCE
# -------------------------------
@app.route("/attendance", methods=["GET", "POST"])
def attendance():

    if request.method == "POST":

        subject = request.form["subject"]

        result = take_attendance(subject)

        if result is None:
            result = "Something went wrong"

        return render_template("result.html", message=result)

    return render_template("subject.html")


# -------------------------------
# CHECK PAGE
# -------------------------------
@app.route("/check")
def check():
    return render_template("check.html")


# -------------------------------
# VERIFY + DASHBOARD
# -------------------------------
@app.route("/verify", methods=["POST"])
def verify():

    name = request.form["name"]
    roll = request.form["roll"]

    if verify_face(roll):

        if not os.path.exists("attendance.csv") or os.stat("attendance.csv").st_size == 0:
            return render_template("result.html", message="No attendance records found")

        df = pd.read_csv("attendance.csv")

        if "Roll" not in df.columns:
            df.columns = ["Name", "Roll", "Subject", "Date", "Time"]

        student = df[df["Roll"].astype(str) == str(roll)]

        if student.empty:
            return render_template("result.html", message="No attendance found")

        data = student.to_dict(orient="records")

        # 🔥 TOTAL DAYS IN CURRENT MONTH
        now = datetime.now()
        total_days = calendar.monthrange(now.year, now.month)[1]

        # 🔥 SUBJECT-WISE COUNT
        subject_count = student.groupby("Subject").size().to_dict()

        return render_template(
            "attendance_view.html",
            name=name,
            roll=roll,
            data=data,
            subject_count=subject_count,
            total_days=total_days
        )

    return render_template("result.html", message="Face not matched")


# -------------------------------
# RUN
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True)