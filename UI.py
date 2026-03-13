import customtkinter as ctk
from register import register_student
from camera import start_camera

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


def open_register():

    reg = ctk.CTkToplevel(app)
    reg.title("Register Student")
    reg.geometry("350x300")

    title = ctk.CTkLabel(reg, text="Register Student", font=("Arial",20))
    title.pack(pady=20)

    name_entry = ctk.CTkEntry(reg, placeholder_text="Enter Student Name")
    name_entry.pack(pady=10)

    roll_entry = ctk.CTkEntry(reg, placeholder_text="Enter Roll Number")
    roll_entry.pack(pady=10)

    status = ctk.CTkLabel(reg, text="")
    status.pack(pady=5)

    def capture():

        name = name_entry.get()
        roll = roll_entry.get()

        if name == "" or roll == "":
            status.configure(text="Please enter details")
            return

        reg.destroy()
        register_student(name, roll)

    capture_btn = ctk.CTkButton(reg, text="Capture Face", command=capture)
    capture_btn.pack(pady=20)


def take_attendance():

    start_camera()


app = ctk.CTk()
app.title("Secure Face Authentication System")
app.geometry("500x400")

title = ctk.CTkLabel(app,
                     text="Face Authentication Attendance",
                     font=("Arial",24))
title.pack(pady=40)

register_btn = ctk.CTkButton(app,
                             text="Register Student",
                             width=200,
                             height=40,
                             command=open_register)
register_btn.pack(pady=10)

attendance_btn = ctk.CTkButton(app,
                               text="Take Attendance",
                               width=200,
                               height=40,
                               command=take_attendance)
attendance_btn.pack(pady=10)

exit_btn = ctk.CTkButton(app,
                         text="Exit",
                         width=200,
                         height=40,
                         fg_color="red",
                         command=app.destroy)
exit_btn.pack(pady=20)

app.mainloop()