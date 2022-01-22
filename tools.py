import os
import sys
import cv2
import time
from dotenv import load_dotenv

load_dotenv()

cam_video_url = os.getenv('URL_CAM1')


def guardar_imagen_evento(cv2, frame):
	if not os.path.isfile("images/event.jpg"):
		#     # cv2.imshow("event", frame)
		cv2.imwrite("images/event.jpg", frame)


def take_a_picture():
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


def record_a_video():
	print("Recording a 10seconds video..")
	# Video settings
	fps = 30
	width = 864
	height = 640
	video_codec = cv2.VideoWriter_fourcc("D", "I", "V", "X")
	# name = time.strftime("VID_%Y%m%d_%H%M%S", time.localtime())
	video_file = "videos/event.mp4"

	cap = cv2.VideoCapture(cam_video_url)
	ret = cap.set(3, 864)
	ret = cap.set(4, 480)

	start = time.time()
	video_file_count = 0
	print("Capture video saved location : {}".format(video_file))

	# Create a video write before entering the loop
	video_writer = cv2.VideoWriter(
		video_file, video_codec, fps, (int(cap.get(3)), int(cap.get(4)))
	)

	while cap.isOpened():
		ret, frame = cap.read()
		if ret is True:
			# cv2.imshow("frame", frame)  # Muestra la captura
			if time.time() - start > 10:
				if video_file_count < 1:
					start = time.time()
					video_writer = cv2.VideoWriter(
						video_file, video_codec, fps, (int(cap.get(3)), int(cap.get(4)))
					)
					video_file_count += 1
				# No sleeping! We don't want to sleep, we want to write
				# time.sleep(10)
				else:
					break  # End process

			# Write the frame to the current video writer
			video_writer.write(frame)
			if cv2.waitKey(1) & 0xFF == ord("q"):
				break
		else:
			break
	cap.release()

