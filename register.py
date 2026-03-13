import cv2
import csv
import os

# Load face detector
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades +
                                     "haarcascade_frontalface_default.xml")

# Load eye detector
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades +
                                    "haarcascade_eye.xml")


def register_student(name, roll):

    cap = cv2.VideoCapture(0)

    eyes_closed = False
    blink_detected = False

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray,1.3,5)

        for (x,y,w,h) in faces:

            # Green rectangle on face
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)

            roi_gray = gray[y:y+h, x:x+w]
            roi_color = frame[y:y+h, x:x+w]

            eyes = eye_cascade.detectMultiScale(roi_gray,1.1,4)

            # Blue rectangle on eyes
            for (ex,ey,ew,eh) in eyes:
                cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(255,0,0),2)

            # Blink detection
            if len(eyes) == 0:
                eyes_closed = True

            if eyes_closed and len(eyes) > 0:
                blink_detected = True

        if blink_detected:
            cv2.putText(frame,"Blink detected - Press C to capture",
                        (20,40),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7,
                        (0,255,0),
                        2)
        else:
            cv2.putText(frame,"Please blink to verify",
                        (20,40),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7,
                        (0,0,255),
                        2)

        cv2.imshow("Register Student",frame)

        key = cv2.waitKey(1)

        if key == ord('c') and blink_detected:

            if not os.path.exists("dataset"):
                os.makedirs("dataset")

            # save image
            path = f"dataset/{roll}_{name}.jpg"
            cv2.imwrite(path,frame)

            # save student details
            with open("students.csv","a",newline="") as f:
                writer = csv.writer(f)
                writer.writerow([roll,name])

            print("Student Registered")

            break

        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()