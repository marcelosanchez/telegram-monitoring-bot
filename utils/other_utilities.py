import time
from datetime import datetime, timedelta
from constants.settings_constants import GMT_DELTA


def get_time_delta_seconds(time_now):
	if isinstance(time_now, float):
		pass
	else:
		raise ValueError("El argumento 'time_now' debe ser un 'float' (time.time()).")

	delta_time = timedelta(hours=GMT_DELTA)
	new_time = datetime.fromtimestamp(time_now) + delta_time
	# print("🕒 Time now: " + str(new_time))

	return new_time.timestamp()


def get_datetime_delta(time_now):
	if isinstance(time_now, datetime):
		pass
	else:
		raise ValueError("El argumento 'time_now' debe ser un objeto 'datetime' (datetime.now()).")

	delta_time = timedelta(hours=GMT_DELTA)
	new_time = time_now + delta_time
	# print("🕒 Time now: " + str(new_time))

	return new_time


def is_called_on_group(update):
	# Validation to work only in groups
	return update.message.chat.type == 'group' or update.message.chat.type == 'supergroup'
