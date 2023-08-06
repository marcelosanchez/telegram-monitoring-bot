import numpy as np

from constants.paths_constants import SUMMARY, EVENT
from constants.settings_constants import *
from utils.other_utilities import *


# global variables
CAM_URL = URL_CAM1

DATE_FORMAT     = TIME_FORMATS["SHORT"]
DATETIME_FORMAT = TIME_FORMATS["LONG"]

# video record
VIDEO_RECORD_FRAME_WIDTH  = VIDEO["RECORD"]["FRAME_WIDTH"]
VIDEO_RECORD_FRAME_HEIGHT = VIDEO["RECORD"]["FRAME_HEIGHT"]
VIDEO_RECORD_FPS          = VIDEO["RECORD"]["FPS"]

VIDEO_CODEC = VIDEO["CODEC"]

EVENT_IMAGE_FILE_PATH = EVENT["IMAGE"]["RELATIVE_PATH"]
EVENT_IMAGE_FILE_NAME = EVENT["IMAGE"]["FILE_NAME"]
EVENT_VIDEO_FILE_PATH = EVENT["VIDEO"]["FULL_PATH"]
EVENT_VIDEO_RELATIVE_PATH = EVENT["VIDEO"]["RELATIVE_PATH"]

SUMMARY_IMAGE_FILE_PATH = SUMMARY["IMAGE"]["FULL_PATH"]
SUMMARY_VIDEO_FILE_PATH = SUMMARY["VIDEO"]["FULL_PATH"]

PATH_LAST_SUMMARY_DATE = SUMMARY["LOG"]["FULL_PATH"]


def take_a_picture():
	icap = cv2.VideoCapture(CAM_URL)  # 1
	i = 0
	while icap.isOpened():
		ret, frame = icap.read()

		# This condition prevents from infinite looping
		# incase video ends.
		if not ret:
			break

		# Save Frame by Frame into disk using imwrite method
		save_event_captured(frame)
		i += 1

		if i >= 1:
			break

	icap.release()


def save_event_captured(frame):
	now = get_datetime_delta(datetime.now())

	summary_image_filename = now.strftime(DATETIME_FORMAT) + ".jpg"
	summary_image_path = os.path.join(SUMMARY_IMAGE_FILE_PATH, now.strftime(DATE_FORMAT))

	save_picture_captured(summary_image_path, summary_image_filename, frame)  # summary/*.jpg
	save_picture_captured(EVENT_IMAGE_FILE_PATH, EVENT_IMAGE_FILE_NAME, frame)  # event.jpg


def save_picture_captured(path, filename, frame):
	if not os.path.exists(path):
		os.makedirs(path)
	picture_path = os.path.join(path, filename)
	cv2.imwrite(picture_path, frame)


def record_a_video(record_time_sec):
	print("🎬 Recording a " + str(record_time_sec) + " seconds video..")
	cv2.waitKey(int(1000 / VIDEO_RECORD_FPS - 1))
	vcap = cv2.VideoCapture(CAM_URL)
	vcap.set(cv2.CAP_PROP_FPS, VIDEO_RECORD_FPS)
	vcap.set(cv2.CAP_PROP_FRAME_WIDTH, VIDEO_RECORD_FRAME_WIDTH)
	vcap.set(cv2.CAP_PROP_FRAME_HEIGHT, VIDEO_RECORD_FRAME_HEIGHT)
	vcap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

	print("Captured video saved on: {}".format(EVENT_VIDEO_FILE_PATH))

	# Create a video write before entering the loop
	video_writer_out = cv2.VideoWriter(
		EVENT_VIDEO_FILE_PATH, VIDEO_CODEC, VIDEO_RECORD_FPS, (int(vcap.get(3)), int(vcap.get(4)))
	)

	start_time = get_time_delta_seconds(time.time())
	while int(get_time_delta_seconds(time.time()) - start_time) <= int(record_time_sec - 1):
		# print(time.time() - start_time)
		ret, frame = vcap.read()
		if ret is True:
			# frame = cv2.flip(frame, 0)
			video_writer_out.write(frame)
			# time.sleep(1)  # 1s/30fps = 0.03

			if cv2.waitKey(1) & 0xFF == ord("q"):
				break
		else:
			break
	vcap.release()
	video_writer_out.release()
	print("Record Finished...")
	video_duration(EVENT_VIDEO_FILE_PATH)


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
		last_modification_time = get_time_delta_seconds(os.path.getmtime(path_to_file))
		last = datetime.fromtimestamp(last_modification_time)
		now = get_datetime_delta(datetime.now())
		difference = (now - last)
		total_seconds = difference.total_seconds()

		if total_seconds < diff_seconds:
			return False
		return True
	return False


def video_duration(path_to_video):
	import datetime

	# create video capture object
	data = cv2.VideoCapture(path_to_video)

	# count the number of frames
	frames = data.get(cv2.CAP_PROP_FRAME_COUNT)
	fps = int(data.get(cv2.CAP_PROP_FPS))

	# Verify fps is valid
	if fps == 0:
		return 0

	# calculate dusration of the video
	seconds = int(frames / fps)
	video_time = str(datetime.timedelta(seconds=seconds))
	print("🕔 Video duration:", video_time)


def get_file_size_in_mb(path_to_file):
	size = os.path.getsize(path_to_file)
	size_in_mb = size / (1024 * 1024)
	return size_in_mb


def storage_video(event_video):
	now = get_datetime_delta(datetime.now())
	# Validar directorio para los videos
	date_str = now.strftime(TIME_FORMAT_SHORT)
	datetime_str = now.strftime(TIME_FORMAT_LONG)

	today_video_path = os.path.join(EVENT_VIDEO_RELATIVE_PATH, date_str)
	if not os.path.exists(today_video_path):
		os.makedirs(today_video_path)

	os.rename(event_video, os.path.join(today_video_path, datetime_str + ".mp4"))
	print("Video moved to: ", today_video_path, " as ", datetime_str + ".mp4")
	return datetime_str + ".mp4"
