import cv2
import os
import csv
from datetime import datetime
from deepface import DeepFace

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

dataset_path = "dataset"

recognized_name = "Unknown"
recognized_roll = ""


def mark_attendance(name, roll):

    now = datetime.now()
    time = now.strftime("%H:%M:%S")

    with open("attendance.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([name, roll, time])


def recognize_face(face_img):

    best_match = "Unknown"
    best_roll = ""
    best_distance = 1

    for file in os.listdir(dataset_path):

        path = os.path.join(dataset_path, file)

        try:

            result = DeepFace.verify(
                face_img,
                path,
                model_name="Facenet",
                enforce_detection=False
            )

            distance = result["distance"]

            if distance < best_distance and distance < 0.35:

                best_distance = distance

                roll, name = file.split("_")
                name = name.split(".")[0]

                best_match = name
                best_roll = roll

        except:
            pass

    return best_match, best_roll


def start_camera():

    global recognized_name
    global recognized_roll

    cap = cv2.VideoCapture(0)

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:

            cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)

            face_img = frame[y:y+h, x:x+w]

            recognized_name, recognized_roll = recognize_face(face_img)

            cv2.putText(frame,
                        recognized_name,
                        (x, y-10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.9,
                        (0,255,0),
                        2)

        cv2.putText(frame,
                    "Press C to mark attendance",
                    (20,40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0,255,255),
                    2)

        cv2.imshow("Attendance Camera", frame)

        key = cv2.waitKey(1)

        if key == ord('c'):

            if recognized_name != "Unknown":

                mark_attendance(recognized_name, recognized_roll)

                print("Attendance Recorded")

                break

        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()