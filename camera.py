import cv2
from deepface import DeepFace
import pandas as pd
from datetime import datetime
import os
import winsound

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

def beep_success():
    winsound.Beep(1500,300)

def beep_fail():
    winsound.Beep(500,500)


def take_attendance(subject):

    if not os.path.exists("attendance.csv"):
        df = pd.DataFrame(columns=["Name","Roll","Subject","Date","Time"])
        df.to_csv("attendance.csv", index=False)

    df = pd.read_csv("attendance.csv")
    students = pd.read_csv("students.csv")

    cap = cv2.VideoCapture(0)
    cap.set(3,480)
    cap.set(4,360)

    recognized_roll = None
    recognized_name = None

    stable_frames = 0
    frame_count = 0

    while True:

        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1
        current_time = datetime.now().strftime("%H:%M:%S")

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray,1.3,5)

        for (x,y,w,h) in faces:

            face_img = frame[y:y+h, x:x+w]
            small_face = cv2.resize(face_img, (160,160))

            if frame_count % 5 == 0:
                try:
                    result = DeepFace.find(
                        img_path=small_face,
                        db_path="dataset",
                        enforce_detection=False,
                        model_name="Facenet"
                    )

                    if len(result[0]) > 0:
                        best = result[0].iloc[0]

                        if best["distance"] < 0.55:
                            identity = best["identity"]
                            roll = os.path.basename(os.path.dirname(identity))

                            name = students.loc[
                                students["Roll"].astype(str)==str(roll),"Name"
                            ].values[0]

                            recognized_roll = roll
                            recognized_name = name
                        else:
                            recognized_roll = None
                            recognized_name = None

                except:
                    pass

            if recognized_roll:
                stable_frames += 1
            else:
                stable_frames = 0

            label = "Unknown"
            color = (0,0,255)

            if recognized_roll:
                label = f"{recognized_name} ({recognized_roll})"
                color = (0,255,0)

            cv2.rectangle(frame,(x,y),(x+w,y+h),color,2)
            cv2.putText(frame,label,(x,y-10),
                        cv2.FONT_HERSHEY_SIMPLEX,0.8,color,2)

        if stable_frames < 15:
            cv2.putText(frame,"Hold Still...",(20,80),
                        cv2.FONT_HERSHEY_SIMPLEX,0.8,(0,255,255),2)
        else:
            cv2.putText(frame,"Press C to Capture",(20,80),
                        cv2.FONT_HERSHEY_SIMPLEX,0.8,(0,255,0),2)

        cv2.putText(frame,f"Time: {current_time}",(20,40),
                    cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,255,255),2)

        cv2.imshow("Attendance Camera", frame)

        key = cv2.waitKey(1)

        if key == ord('c') and stable_frames >= 15:

            if recognized_roll:

                today = datetime.now().strftime("%Y-%m-%d")

                exists = df[
                    (df["Roll"].astype(str)==str(recognized_roll)) &
                    (df["Subject"]==subject) &
                    (df["Date"]==today)
                ]

                if not exists.empty:
                    beep_fail()
                    cap.release()
                    cv2.destroyAllWindows()
                    return "Already marked today"

                time_now = datetime.now().strftime("%H:%M:%S")

                new_row = {
                    "Name": recognized_name,
                    "Roll": recognized_roll,
                    "Subject": subject,
                    "Date": today,
                    "Time": time_now
                }

                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                df.to_csv("attendance.csv", index=False)

                beep_success()
                cap.release()
                cv2.destroyAllWindows()
                return f"Attendance marked for {recognized_name}"

            else:
                beep_fail()
                cap.release()
                cv2.destroyAllWindows()
                return "Face not recognized"

        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return "Camera closed"