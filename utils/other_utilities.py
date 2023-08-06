import time
from datetime import datetime, timedelta

from constants.settings_constants import GMT_DELTA, TIME_FORMATS

DATE_FORMAT = TIME_FORMATS["SHORT"]


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


def get_today():
	day = get_datetime_delta(datetime.now())
	day = day.strftime(DATE_FORMAT)
	return day


def get_past_day(offset_days=0):
	today = get_datetime_delta(datetime.now())
	specific_date = today - timedelta(days=offset_days)
	return specific_date.strftime(DATE_FORMAT)


def get_now_datetime_str(format_option):
	today = get_datetime_delta(datetime.now())
	today = today.strftime(TIME_FORMATS[format_option])
	return today


def is_called_on_group(update):
	# Validation to work only in groups
	return update.message.chat.type == 'group' or update.message.chat.type == 'supergroup'
