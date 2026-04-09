from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
import os
import bcrypt
from datetime import datetime, timedelta

from camera import take_attendance
from register import capture_face

app = Flask(__name__)
app.secret_key = "secure_key_123"

# 🔐 LOGIN TRACKING
login_attempts = {}
lock_time = {}
LOCK_DURATION = 5  # minutes


# ---------------- HOME ----------------
@app.route("/")
def home():
    return render_template("index.html")


# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():

    global login_attempts, lock_time

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"].encode()

        # initialize
        if username not in login_attempts:
            login_attempts[username] = 0

        # 🔒 check if locked
        if username in lock_time:
            if datetime.now() < lock_time[username]:
                remaining = (lock_time[username] - datetime.now()).seconds // 60
                return render_template("login.html",
                    message=f"Account locked! Try again in {remaining} min")
            else:
                # unlock automatically
                login_attempts[username] = 0
                del lock_time[username]

        if not os.path.exists("admin.csv"):
            return "admin.csv not found"

        df = pd.read_csv("admin.csv")

        admin = df[df["username"] == username]

        if not admin.empty:
            stored_password = admin.iloc[0]["password"].encode()

            if bcrypt.checkpw(password, stored_password):
                login_attempts[username] = 0
                session["admin"] = username
                return redirect(url_for("admin_dashboard"))

        # ❌ wrong password
        login_attempts[username] += 1

        if login_attempts[username] >= 3:
            lock_time[username] = datetime.now() + timedelta(minutes=LOCK_DURATION)
            return render_template("login.html",
                message="Account locked for 5 minutes!")

        remaining = 3 - login_attempts[username]
        return render_template("login.html",
            message=f"Invalid credentials! {remaining} attempts left")

    return render_template("login.html")


# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect(url_for("login"))


# ---------------- REGISTER ----------------
@app.route("/register", methods=["GET","POST"])
def register():

    if "admin" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        name = request.form["name"]
        roll = request.form["roll"]

        result = capture_face(name, roll)

        if result:
            return render_template("result.html", message="Student Registered Successfully")
        else:
            return render_template("result.html", message="Registration Cancelled")

    return render_template("register.html")


# ---------------- ATTENDANCE ----------------
@app.route("/attendance", methods=["GET","POST"])
def attendance():

    if request.method == "POST":
        subject = request.form["subject"]
        result = take_attendance(subject)
        return render_template("result.html", message=result)

    return render_template("subject.html")


# ---------------- ADMIN DASHBOARD ----------------
@app.route("/admin", methods=["GET","POST"])
def admin_dashboard():

    if "admin" not in session:
        return redirect(url_for("login"))

    students = []
    selected_attendance = []
    show_students = False
    attendance_percentage = {}

    if os.path.exists("students.csv"):
        students_df = pd.read_csv("students.csv")
        students = students_df.to_dict(orient="records")
    else:
        students_df = pd.DataFrame()

    if os.path.exists("attendance.csv"):
        attendance_df = pd.read_csv("attendance.csv")
    else:
        attendance_df = pd.DataFrame()

    # 📊 percentage
    if not attendance_df.empty and not students_df.empty:
        total_days = attendance_df["Date"].nunique()

        for student in students:
            roll = str(student["Roll"])

            count = attendance_df[
                attendance_df["Roll"].astype(str) == roll
            ].shape[0]

            percentage = round((count / total_days) * 100, 2) if total_days > 0 else 0
            attendance_percentage[roll] = percentage

    if request.method == "POST":
        action = request.form.get("action")

        if action == "view_students":
            show_students = True

        elif action == "view_attendance":
            roll = request.form["roll"]

            if not attendance_df.empty:
                filtered = attendance_df[
                    attendance_df["Roll"].astype(str) == str(roll)
                ]
                selected_attendance = filtered.to_dict(orient="records")

    return render_template(
        "admin_dashboard.html",
        students=students,
        selected_attendance=selected_attendance,
        show_students=show_students,
        attendance_percentage=attendance_percentage
    )


# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)