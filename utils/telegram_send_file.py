import asyncio
import os
import pyrogram

from constants.settings_constants import TELEGRAM_API_ID, TELEGRAM_API_HASH, BOT_TELEGRAM_TOKEN, GROUP_ID
from utils.pyrogram_client import send_message


def send_to_telegram(file_path, file_type, caption):
	"""
	Send a photo to a Telegram chat.
	"""
	# file_path = "./media/record/pictures/event.jpg"
	# file_type = "photo"
	# caption = "test"
	try:
		# Event loop creation
		loop = asyncio.new_event_loop()
		asyncio.set_event_loop(loop)

		# Create and start the client
		with pyrogram.Client(
				"my_bot",
				api_id=TELEGRAM_API_ID,
				api_hash=TELEGRAM_API_HASH,
				bot_token=BOT_TELEGRAM_TOKEN
		) as client:
			send_message(file_path, file_type, client, GROUP_ID, caption)

		# Remove the temporary file after sending
		# remove_temp_file(file_path)

	except Exception as error_msg:
		print("send_to_telegram | error: ", str(error_msg))
		pass


def remove_temp_file(file_path):
	"""
	Remove the temporary file.
	"""
	print("Removing temporary file: ", file_path)
	os.remove(file_path)

