import os
from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '')

EVENT = {
	"IMAGE": {
		"PATH": os.getenv('RECORDS_PICTURE_PATH'),
		"FILE_NAME": os.getenv('RECORDS_PICTURE_FILENAME'),
		"RELATIVE_PATH": os.path.join(PROJECT_ROOT_PATH, os.getenv('RECORDS_PICTURE_PATH')),
		"FULL_PATH": os.path.join(PROJECT_ROOT_PATH, os.getenv('RECORDS_PICTURE_PATH'), os.getenv('RECORDS_PICTURE_FILENAME')),
	},
	"VIDEO": {
		"PATH": os.getenv('RECORDS_VIDEO_PATH'),
		"FILE_NAME": os.getenv('RECORDS_VIDEO_FILENAME'),
		"RELATIVE_PATH": os.path.join(PROJECT_ROOT_PATH, os.getenv('RECORDS_VIDEO_PATH')),
		"FULL_PATH": os.path.join(PROJECT_ROOT_PATH, os.getenv('RECORDS_VIDEO_PATH'), os.getenv('RECORDS_VIDEO_FILENAME')),
	},
}

SUMMARY = {
	"IMAGE": {
		"PATH": os.getenv('SUMMARY_PICTURE_PATH'),
		"FULL_PATH": os.path.join(PROJECT_ROOT_PATH, os.getenv('SUMMARY_PICTURE_PATH')),
	},
	"VIDEO": {
		"PATH": os.getenv('SUMMARY_VIDEO_PATH'),
		"FULL_PATH": os.path.join(PROJECT_ROOT_PATH, os.getenv('SUMMARY_VIDEO_PATH')),
	},
}
