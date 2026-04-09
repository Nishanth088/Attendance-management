import cv2
import os
import pandas as pd


def capture_face(name, roll):

    dataset_path = "dataset"

    # create dataset folder
    if not os.path.exists(dataset_path):
        os.makedirs(dataset_path)

    student_folder = os.path.join(dataset_path, str(roll))

    if not os.path.exists(student_folder):
        os.makedirs(student_folder)

    # ----------------------------
    # SAVE STUDENT DETAILS
    # ----------------------------
    if not os.path.exists("students.csv"):
        df = pd.DataFrame(columns=["Name", "Roll"])
        df.to_csv("students.csv", index=False)

    df = pd.read_csv("students.csv")

    # prevent duplicate roll
    if roll in df["Roll"].astype(str).values:
        print("Student already exists")
        return False

    new_student = {
        "Name": name,
        "Roll": roll
    }

    df = pd.concat([df, pd.DataFrame([new_student])], ignore_index=True)
    df.to_csv("students.csv", index=False)

    # ----------------------------
    # START CAMERA
    # ----------------------------
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)

    count = 0
    capturing = False

    while True:

        ret, frame = cap.read()
        if not ret:
            break

        if not capturing:
            cv2.putText(frame, "Press C to Start Capture", (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
        else:
            cv2.putText(frame, f"Capturing {count}/30", (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        cv2.imshow("Register Face", frame)

        key = cv2.waitKey(1)

        # START CAPTURE
        if key == ord('c') and not capturing:
            capturing = True

        # AUTO CAPTURE
        if capturing:
            count += 1

            img_path = os.path.join(student_folder, f"{count}.jpg")
            cv2.imwrite(img_path, frame)

            cv2.waitKey(100)

            if count >= 30:
                cap.release()
                cv2.destroyAllWindows()
                return True   # SUCCESS

        # CANCEL
        if key == ord('q'):
            cap.release()
            cv2.destroyAllWindows()

            # 🔥 REMOVE PARTIAL DATA
            if os.path.exists(student_folder):
                for file in os.listdir(student_folder):
                    os.remove(os.path.join(student_folder, file))
                os.rmdir(student_folder)

            return False  # CANCELLED

    cap.release()
    cv2.destroyAllWindows()
    return False