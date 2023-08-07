import os
import cv2
from dotenv import load_dotenv

load_dotenv()

URL_CAM1 = os.getenv('URL_CAM1')
BOT_TELEGRAM_TOKEN = os.getenv('BOT_TELEGRAM_TOKEN')

TELEGRAM_API_ID = os.getenv('TELEGRAM_API_ID')
TELEGRAM_API_HASH = os.getenv('TELEGRAM_API_HASH')
GROUP_ID = int(os.getenv('GROUP_ID'))

GMT_DELTA = int(os.getenv('GMT_DELTA') if os.getenv('GMT_DELTA') else 0)

EVENT_DETECT_POINTS = int(os.getenv('EVENT_DETECT_POINTS'))

TIME_FORMAT_SHORT = "%Y%m%d"
TIME_FORMAT_LONG = "%Y%m%d_%H%M%S"
TIME_FORMAT_PRETTY_SHORT = "%Y-%m-%d"
TIME_FORMAT_PRETTY_LONG = "%Y-%m-%d %H:%M:%S"

TIME_FORMATS = {
	"SHORT": TIME_FORMAT_SHORT,
	"LONG": TIME_FORMAT_LONG,
	"PRETTY_SHORT": TIME_FORMAT_PRETTY_SHORT,
	"PRETTY_LONG": TIME_FORMAT_PRETTY_LONG,
}

BOT_TIMEOUT = {
	"IMAGE": int(os.getenv('TIMEOUT_EVENT_IMAGE')),
	"VIDEO": int(os.getenv('TIMEOUT_EVENT_VIDEO')),
	"SUMMARY": int(os.getenv('TIMEOUT_SUMMARY_EVENT')),
}

BOT_WAIT_TIMEOUT = {
	"IMAGE": int(os.getenv('IMG_WAIT_TIME'))
}

VIDEO = {
	"RECORD": {
		"FRAME_WIDTH": int(os.getenv('VIDEO_RECORD_FRAME_WIDTH')),
		"FRAME_HEIGHT": int(os.getenv('VIDEO_RECORD_FRAME_HEIGHT')),
		"FPS": int(os.getenv('VIDEO_RECORD_FPS')),

		"DEFAULT_RECORD_TIME": int(os.getenv('DEFAULT_RECORD_TIME')),
		"EVENT_RECORD_TIME": int(os.getenv('EVENT_RECORD_TIME')),
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

MEDIA_PHOTO = "photo"
MEDIA_VIDEO = "video"
