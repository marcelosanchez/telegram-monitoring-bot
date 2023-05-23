import os
import cv2
from dotenv import load_dotenv

load_dotenv()

URL_CAM1 = os.getenv('URL_CAM1')
BOT_TELEGRAM_TOKEN = os.getenv('BOT_TELEGRAM_TOKEN')

GMT_DELTA = int(os.getenv('GMT_DELTA') if os.getenv('GMT_DELTA') else 0)

EVENT_DETECT_POINTS = int(os.getenv('EVENT_DETECT_POINTS'))

TIME_FORMAT_SHORT = "%Y%m%d"
TIME_FORMAT_LONG = "%Y%m%d_%H%M%S"

BOT_TIMEOUT = {
	"IMAGE": int(os.getenv('TIMEOUT_EVENT_IMAGE')),
	"VIDEO": int(os.getenv('TIMEOUT_EVENT_VIDEO')),
}

VIDEO = {
	"RECORD": {
		"FRAME_WIDTH": int(os.getenv('VIDEO_RECORD_FRAME_WIDTH')),
		"FRAME_HEIGHT": int(os.getenv('VIDEO_RECORD_FRAME_HEIGHT')),
		"FPS": int(os.getenv('VIDEO_RECORD_FPS')),

		"DEFAULT_RECORD_TIME": int(os.getenv('DEFAULT_RECORD_TIME')),
	},
	"SUMMARY": {
		"FRAME_WIDTH": int(os.getenv('VIDEO_SUMMARY_FRAME_WIDTH')),
		"FRAME_HEIGHT": int(os.getenv('VIDEO_SUMMARY_FRAME_HEIGHT')),
		"FPS": int(os.getenv('VIDEO_SUMMARY_FPS')),

		"PRESERVE_RECORDS_DAYS": int(os.getenv('PRESERVE_RECORDS_DAYS')),
	},
	"CODEC": cv2.VideoWriter_fourcc(*'mp4v'),
}

PICTURE = {
	"QUALITY": int(os.getenv('PICTURE_QUALITY')),
}



