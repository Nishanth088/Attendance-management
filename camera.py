import cv2
from deepface import DeepFace
import pandas as pd
from datetime import datetime
import os

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)


def take_attendance(subject):

    cap = cv2.VideoCapture(0)
    cap.set(3, 480)
    cap.set(4, 360)

    df = pd.read_csv("attendance.csv")
    students = pd.read_csv("students.csv")

    recognized_roll = None
    recognized_name = None
    frame_count = 0

    while True:

        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray,1.3,5)

        for (x,y,w,h) in faces:

            face_img = frame[y:y+h, x:x+w]
            small_face = cv2.resize(face_img, (160,160))

            if frame_count % 8 == 0:

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
                label = f"{recognized_name} ({recognized_roll})"
                color = (0,255,0)
            else:
                label = "Unknown"
                color = (0,0,255)

            cv2.rectangle(frame,(x,y),(x+w,y+h),color,2)
            cv2.putText(frame,label,(x,y-10),
                        cv2.FONT_HERSHEY_SIMPLEX,0.9,color,2)

        cv2.putText(frame,"Press C to Capture",(20,40),
                    cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)

        cv2.imshow("Attendance Camera", frame)

        key = cv2.waitKey(5)

        if key == ord('c'):

            if recognized_roll:

                today = datetime.now().strftime("%Y-%m-%d")

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

                cap.release()
                cv2.destroyAllWindows()
                return f"Attendance saved for {recognized_name}"

            else:
                cap.release()
                cv2.destroyAllWindows()
                return "Face not recognized"

        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return "Camera closed"


def verify_face(roll):

    cap = cv2.VideoCapture(0)

    while True:

        ret, frame = cap.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray,1.3,5)

        for (x,y,w,h) in faces:

            face_img = frame[y:y+h, x:x+w]
            small_face = cv2.resize(face_img, (160,160))

            try:
                result = DeepFace.find(
                    img_path=small_face,
                    db_path=f"dataset/{roll}",
                    enforce_detection=False,
                    model_name="Facenet"
                )

                if len(result[0]) > 0:
                    best = result[0].iloc[0]

                    if best["distance"] < 0.55:
                        cap.release()
                        cv2.destroyAllWindows()
                        return True

            except:
                pass

        cv2.imshow("Verification", frame)

        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return False