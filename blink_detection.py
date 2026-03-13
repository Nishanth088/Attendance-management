import cv2

# load eye detector
eye_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_eye.xml"
)

eyes_closed_frames = 0
blink_detected = False


def detect_blink(frame):

    global eyes_closed_frames
    global blink_detected

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    eyes = eye_cascade.detectMultiScale(gray, 1.1, 4)

    # if no eyes detected → eyes closed
    if len(eyes) == 0:
        eyes_closed_frames += 1

    else:

        # if eyes reopen after being closed
        if eyes_closed_frames > 3:
            blink_detected = True

        eyes_closed_frames = 0

    return blink_detected