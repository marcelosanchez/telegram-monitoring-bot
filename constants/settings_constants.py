import os
import cv2

URL_CAM1 = os.getenv('URL_CAM1')
BOT_TELEGRAM_TOKEN = os.getenv('BOT_TELEGRAM_TOKEN')

GMT_DELTA = os.getenv('GMT_DELTA')

EVENT_DETECT_POINTS = os.getenv('EVENT_DETECT_POINTS')

SETTINGS = {
	"VIDEO": {
		"RECORD": {
			"FRAME_WIDTH": os.getenv('VIDEO_RECORD_FRAME_WIDTH'),
			"FRAME_HEIGHT": os.getenv('VIDEO_RECORD_FRAME_HEIGHT'),
			"FPS": os.getenv('VIDEO_RECORD_FPS'),

			"DEFAULT_RECORD_TIME": os.getenv('DEFAULT_RECORD_TIME'),
		},
		"SUMMARY": {
			"FRAME_WIDTH": os.getenv('VIDEO_SUMMARY_FRAME_WIDTH'),
			"FRAME_HEIGHT": os.getenv('VIDEO_SUMMARY_FRAME_HEIGHT'),
			"FPS": os.getenv('VIDEO_SUMMARY_FPS'),

			"PRESERVE_RECORDS_DAYS": os.getenv('PRESERVE_RECORDS_DAYS'),
		},
		"CODEC": cv2.VideoWriter_fourcc(*'mp4v'),
	},
	"PICTURE": {
		"QUALITY": os.getenv('PICTURE_QUALITY'),
	}
}

PATHS = {
	"IMAGES": {
		"EVENT": os.getenv('PATH_IMAGES_EVENT'),
		"SUMMARY": os.getenv('PATH_IMAGES_SUMMARY'),
	},
	"VIDEOS": {
		"EVENT": os.getenv('PATH_VIDEOS_EVENT'),
		"SUMMARY": os.getenv('PATH_VIDEOS_SUMMARY'),
	},
},



