import os

import cv2
from dotenv import load_dotenv

load_dotenv()

cam_video_url = os.getenv('URL_CAM1')


def guardar_imagen_evento(cv2, frame):
	if not os.path.isfile("images/event.jpg"):
		#     # cv2.imshow("event", frame)
		cv2.imwrite("images/event.jpg", frame)


def guardar_captura_camara():
	cap = cv2.VideoCapture(cam_video_url)  # 1
	i = 0
	while cap.isOpened():
		ret, frame = cap.read()

		# This condition prevents from infinite looping
		# incase video ends.
		if not ret:
			break

		# Save Frame by Frame into disk using imwrite method
		cv2.imwrite("images/event.jpg", frame)
		i += 1

		if i >= 1:
			break

	cap.release()
