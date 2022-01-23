import os
import cv2
import time
from datetime import datetime

import numpy as np
from dotenv import load_dotenv

load_dotenv()

cam_video_url = os.getenv('URL_CAM1')


def guardar_imagen_evento(cv2, frame):
	if not os.path.isfile("images/event.jpg"):
		#     # cv2.imshow("event", frame)
		cv2.imwrite("images/event.jpg", frame)


def take_a_picture():
	icap = cv2.VideoCapture(cam_video_url)  # 1
	i = 0
	while icap.isOpened():
		ret, frame = icap.read()

		# This condition prevents from infinite looping
		# incase video ends.
		if not ret:
			break

		# Save Frame by Frame into disk using imwrite method
		cv2.imwrite("images/event.jpg", frame)
		i += 1

		if i >= 1:
			break

	icap.release()


def record_a_video(record_time_sec):
	print("Recording a " + str(record_time_sec) + " seconds video..")
	# Video settings
	fps = 30
	width = 1280
	height = 720
	video_codec = cv2.VideoWriter_fourcc(*'mp4v')
	# name = time.strftime("VID_%Y%m%d_%H%M%S", time.localtime())
	video_file = "videos/event.mp4"

	vcap = cv2.VideoCapture(cam_video_url)
	retw = vcap.set(3, width)
	reth = vcap.set(4, height)

	print("Captured video saved on: {}".format(video_file))

	# Create a video write before entering the loop
	video_writer_out = cv2.VideoWriter(
		video_file, video_codec, fps, (int(vcap.get(3)), int(vcap.get(4)))
	)

	start_time = time.time()
	while int(time.time() - start_time) <= int(record_time_sec - 1):
		# print(time.time() - start_time)
		ret, frame = vcap.read()
		if ret is True:
			# frame = cv2.flip(frame, 0)
			video_writer_out.write(frame)
			if cv2.waitKey(1) & 0xFF == ord("q"):
				break
		else:
			break
	vcap.release()
	video_writer_out.release()


def is_damaged(image):
	# Calculate standard deviation along y axis; average over all color channels
	stddev = np.mean(np.std(image, axis=0), axis=1)

	# DEBUG
	print('Check Image:', np.mean(stddev))

	if np.mean(stddev) < 30:
		return True

	return False


def required_time_is_completed(path_to_file, diff_seconds):
	if os.path.exists(path_to_file):
		last_modification_time = os.path.getmtime(path_to_file)
		last = datetime.fromtimestamp(last_modification_time)
		now = datetime.now()
		difference = (now - last)
		total_seconds = difference.total_seconds()

		if total_seconds < diff_seconds:
			return False
		return True
	return False
