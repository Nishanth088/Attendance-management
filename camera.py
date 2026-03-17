import cv2
from deepface import DeepFace
import pandas as pd
from datetime import datetime
import os

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)


def verify_face(roll):

    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray,1.3,5)

        for (x,y,w,h) in faces:

            face_img = frame[y:y+h, x:x+w]

            try:
                result = DeepFace.find(
                    img_path=face_img,
                    db_path=f"dataset/{roll}",
                    enforce_detection=False
                )

                if len(result[0]) > 0:
                    best = result[0].iloc[0]

                    if best["distance"] < 0.6:
                        cap.release()
                        cv2.destroyAllWindows()
                        return True

            except:
                pass

        cv2.imshow("Verification",frame)

        if cv2.waitKey(1)==ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return False


def take_attendance(subject):

    cap = cv2.VideoCapture(0)

    if not os.path.exists("attendance.csv") or os.stat("attendance.csv").st_size == 0:
        df = pd.DataFrame(columns=["Name","Roll","Subject","Date","Time"])
        df.to_csv("attendance.csv", index=False)

    df = pd.read_csv("attendance.csv")
    students = pd.read_csv("students.csv")

    recognized_roll = None
    recognized_name = None

    while True:

        ret, frame = cap.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray,1.3,5)

        label = "No Face"
        color = (0,0,255)

        for (x,y,w,h) in faces:

            face_img = frame[y:y+h, x:x+w]

            try:
                result = DeepFace.find(
                    img_path=face_img,
                    db_path="dataset",
                    enforce_detection=False
                )

                if len(result[0]) > 0:

                    best = result[0].iloc[0]

                    if best["distance"] < 0.6:

                        identity = best["identity"]
                        roll = os.path.basename(os.path.dirname(identity))

                        name = students.loc[
                            students["Roll"].astype(str)==str(roll),"Name"
                        ].values[0]

                        recognized_roll = roll
                        recognized_name = name

                        label = f"{name} ({roll})"
                        color = (0,255,0)

                    else:
                        label="Unknown"

            except:
                pass

            cv2.rectangle(frame,(x,y),(x+w,y+h),color,2)
            cv2.putText(frame,label,(x,y-10),
                        cv2.FONT_HERSHEY_SIMPLEX,0.9,color,2)

        cv2.putText(frame,"Press C to Capture",(20,40),
                    cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)

        cv2.imshow("Attendance",frame)

        key = cv2.waitKey(1)

        if key == ord('c'):

            if recognized_roll is not None:

                today = datetime.now().strftime("%Y-%m-%d")

                already = (
                    (df["Roll"].astype(str)==str(recognized_roll)) &
                    (df["Subject"]==subject) &
                    (df["Date"]==today)
                ).any()

                if not already:

                    time = datetime.now().strftime("%H:%M:%S")

                    new_row = {
                        "Name": recognized_name,
                        "Roll": recognized_roll,
                        "Subject": subject,
                        "Date": today,
                        "Time": time
                    }

                    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                    df.to_csv("attendance.csv", index=False)

                    print("Saved:",recognized_name)

            break

    cap.release()
    cv2.destroyAllWindows()