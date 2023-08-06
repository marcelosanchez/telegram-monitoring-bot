import numpy as np
from collections import deque

from constants.paths_constants import EVENT
from utils.cam_utilities import save_picture_captured
from constants.settings_constants import *


CAM_URL             = URL_CAM1
EVENT_DETECT_POINTS = EVENT_DETECT_POINTS
cap = cv2.VideoCapture(CAM_URL)
EVENT_IMAGE_FILE_PATH = EVENT["IMAGE"]["RELATIVE_PATH"]
EVENT_IMAGE_FILE_NAME = EVENT["IMAGE"]["FILE_NAME"]

print("Start video capture...")

sub = cv2.createBackgroundSubtractorMOG2(detectShadows=False)
elemento_estruturante = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
points = deque(maxlen=EVENT_DETECT_POINTS)

while cap.isOpened():
    # ret: is a boolean variable that returns true if the frame is available
    # frame: is an image array vector captured based on the default frames per second defined explicitly or implicitly
    ret, frame = cap.read()

    # This condition prevents from infinite looping
    # incase video ends.
    if not ret:
        print("Video capture finished...")
        break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.blur(gray, (7, 7))

    background_ = sub.apply(gray)
    background_ = cv2.morphologyEx(background_, cv2.MORPH_OPEN, elemento_estruturante, iterations=1)
    background_ = cv2.morphologyEx(background_, cv2.MORPH_CLOSE, elemento_estruturante, iterations=3)
    # print(np.sum(background_))
    if np.sum(background_) < 600000:  # 300000
        if len(points) > 0:
            points.pop()
    else:
        # Se dibuja un circulo en el area de movimiento detectado
        contorno = cv2.findContours(background_, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[0]
        contorno = sorted(contorno, key=cv2.contourArea, reverse=True)[:1]
        (cx, cy), raio = cv2.minEnclosingCircle(contorno[0])
        cv2.circle(frame, (int(cx), int(cy)), int(raio), (0, 255, 0), 2)  # Draw circle
        points.append([int(cx), int(cy)])

        log_msg = "Movement Detected: [" + str(len(points)) + "] points"
        print(log_msg)
        if len(points) >= EVENT_DETECT_POINTS:  # 20
            try:
                import _thread
                _thread.start_new_thread(save_picture_captured, (EVENT_IMAGE_FILE_PATH, EVENT_IMAGE_FILE_NAME, frame))
            except Exception as e:
                print('error :' + str(e))
                pass

        # for (cx1, cy1) in points:
        #     cv2.circle(frame, (int(cx1), int(cy1)), 5, (0, 0, 255), 2)

    # cv2.imshow("video", frame)
    tecla = cv2.waitKey(30)
    if tecla == ord("q"):
        break
