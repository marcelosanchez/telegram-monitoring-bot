import os
import cv2
import glob
import shutil

from constants.paths_constants import SUMMARY
from constants.settings_constants import VIDEO, MEDIA_VIDEO
from utils.other_utilities import get_past_day, get_now_datetime_str, get_today
from utils.telegram_send_file import send_to_telegram


# video summary
SUMMARY_FRAME_WIDTH  = VIDEO["SUMMARY"]["FRAME_WIDTH"]
SUMMARY_FRAME_HEIGHT = VIDEO["SUMMARY"]["FRAME_HEIGHT"]
SUMMARY_VIDEO_FPS    = VIDEO["SUMMARY"]["FPS"]

VIDEO_CODEC = VIDEO["CODEC"]

SUMMARY_IMAGE_FILE_PATH = SUMMARY["IMAGE"]["FULL_PATH"]
SUMMARY_VIDEO_FILE_PATH = SUMMARY["VIDEO"]["FULL_PATH"]

LAST_SUMMARY_FILEPATH = SUMMARY["LOG"]["FULL_PATH"]


def evento_summary(context):
	send_summary_video()


def send_summary_video():

	if has_date_changed():  # new day

		# Verificar si el archivo ya existe en el directorio de destino
		yesterday = get_past_day(1)

		# Validar directorio para los videos
		if not os.path.exists(SUMMARY_VIDEO_FILE_PATH):
			os.makedirs(SUMMARY_VIDEO_FILE_PATH)

		if not os.path.exists(f'{SUMMARY_VIDEO_FILE_PATH}/{yesterday}.mp4'):
			summary_video_path = create_summary_video(yesterday)
			print(f"Summary video created here: {summary_video_path}")

			if summary_video_path is not None:  # video created
				# Send video to Telegram
				caption = "#summary\n" + "`" + get_now_datetime_str("PRETTY_SHORT") + "`"
				send_to_telegram(summary_video_path, MEDIA_VIDEO, caption)

				# Then delete the video
				os.remove(summary_video_path)

				# Also delete the images
				remove_summary_images(yesterday)

				# Update last summary date
				update_last_summary_date()


def has_date_changed():
	if not os.path.exists(LAST_SUMMARY_FILEPATH):
		with open(LAST_SUMMARY_FILEPATH, "w") as f:
			f.write(get_today())
		return False

	with open(LAST_SUMMARY_FILEPATH, "r") as f:
		last_summary_date = f.read().strip()

		return last_summary_date != get_today()


def update_last_summary_date():
	with open(LAST_SUMMARY_FILEPATH, "w") as f:
		f.write(get_today())


def create_summary_video(date_str):
	# Directorio de ayer
	path = f'{SUMMARY_IMAGE_FILE_PATH}/{date_str}/*.jpg'
	# path = f'summary/pictures/{date_str}/*.jpg'
	images = sorted(glob.glob(path))

	# Verificar si existen imágenes del día anterior
	if images:
		# Crear el video de la fecha
		video_name = f'{SUMMARY_VIDEO_FILE_PATH}/{date_str}.mp4'
		# video_name = f'summary/videos/{date_str}.mp4'
		video = cv2.VideoWriter(video_name, VIDEO_CODEC, SUMMARY_VIDEO_FPS, (SUMMARY_FRAME_WIDTH, SUMMARY_FRAME_HEIGHT))
		for image in images:
			video.write(cv2.imread(image))
		cv2.destroyAllWindows()
		video.release()

		return video_name
	else:
		return None


def remove_summary_images(date_str):
	path = f'{SUMMARY_IMAGE_FILE_PATH}/{date_str}'
	if os.path.exists(path):
		shutil.rmtree(path)
