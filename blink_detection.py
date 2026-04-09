import cv2

eye_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_eye.xml"
)

eyes_closed_frames = 0
blink_detected = False
blink_cooldown = 0


def detect_blink(frame):
    global eyes_closed_frames, blink_detected, blink_cooldown

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    eyes = eye_cascade.detectMultiScale(gray, 1.1, 5)

    # cooldown to avoid multiple triggers
    if blink_cooldown > 0:
        blink_cooldown -= 1
        return False

    # eyes closed
    if len(eyes) == 0:
        eyes_closed_frames += 1

    else:
        # blink detected (closed → open)
        if eyes_closed_frames > 2:
            blink_detected = True
            blink_cooldown = 15   # prevent repeated detection

        eyes_closed_frames = 0

    return blink_detected