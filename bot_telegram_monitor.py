"""
Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import signal
import logging
import threading

from telegram import *
from telegram.ext import *

from constants.bot_msg_constants import *
from utils.cam_utilities import *
from utils.summary_utilities import evento_summary
from utils.telegram_send_file import send_to_telegram

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

TOKEN         = BOT_TELEGRAM_TOKEN
img_str       = None
video_str     = None
PATH_IMAGE    = EVENT["IMAGE"]["FULL_PATH"]
PATH_VIDEO    = EVENT["VIDEO"]["FULL_PATH"]
RELATIVE_PATH_VIDEO = EVENT["VIDEO"]["RELATIVE_PATH"]
IMG_WAIT_TIME    = BOT_TIMEOUT["IMAGE"]
VID_WAIT_TIME    = BOT_TIMEOUT["VIDEO"]
VID_SUMMARY_TIME = BOT_TIMEOUT["SUMMARY"]
RECORD_TIME   = VIDEO["RECORD"]["DEFAULT_RECORD_TIME"]

# MESSAGES
START_MONITORING = INLINE_BUTTONS["START"]
STOP_MONITORING  = INLINE_BUTTONS["STOP"]
CAPTURE_IMAGE    = INLINE_BUTTONS["CAPTURE"]
RECORD_VIDEO     = INLINE_BUTTONS["RECORD"]

DATE_FORMAT     = TIME_FORMAT_SHORT
DATETIME_FORMAT = TIME_FORMAT_LONG


# Define a few command handlers. These usually take the two arguments update and
# context.
def read_img():
    # ret, frame = cap.read()
    if os.path.isfile(PATH_IMAGE):
        img_str = open(PATH_IMAGE, "rb")
    else:
        return ""
    return img_str


def read_video():
    # ret, frame = cap.read()
    if os.path.isfile(PATH_VIDEO):
        video_str = open(PATH_VIDEO, "rb")
    else:
        return ""
    return video_str


def evento_img(context):
    chat_id = context.job.context
    binario = read_img()
    if binario != "":
        print("👉🏻 Have a IMG here!")
        context.bot.send_chat_action(chat_id, action=ChatAction.UPLOAD_PHOTO, timeout=IMG_WAIT_TIME)
        context.bot.send_photo(chat_id, photo=binario)

        # caption_str = ""  # "`" + get_now_datetime_str() + "`"
        # send_to_telegram(PATH_IMAGE, MEDIA_PHOTO, caption_str)

        binario.close()
        os.remove(PATH_IMAGE)  # Delete image


def evento_vid(context):
    chat_id = context.job.context
    binario = read_video()
    if binario != "":
        print("👉🏻 Have a VID here!")

        if required_time_is_completed(PATH_VIDEO, VID_WAIT_TIME):
            video_duration(PATH_VIDEO)
            print("Its time to send the video!")
            video_size = get_file_size_in_mb(PATH_VIDEO)
            print("Size: " + str(video_size))

            try:
                caption_str = "#video\n`" + get_now_datetime_str("LONG") + "`"
                context.bot.send_chat_action(chat_id, action=ChatAction.RECORD_VIDEO)
                send_to_telegram(PATH_VIDEO, MEDIA_VIDEO, caption_str)
                os.remove(PATH_VIDEO)  # Delete video

            except TelegramError as e:
                context.bot.send_chat_action(chat_id, action=ChatAction.TYPING, timeout=RECORD_TIME)
                context.bot.send_message(chat_id, text="🙁 Ops! Something went wrong: " + str(e))
                os.remove(PATH_VIDEO)  # Delete video


def shutdown():
    Updater.stop()
    Updater.is_idle = False


def evento_sum(context):
    evento_summary(context.job.context)


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    # Validation to work only in groups
    if not is_called_on_group(update):
        return
    context.job_queue.run_repeating(evento_img, interval=IMG_WAIT_TIME, first=1, context=update.message.chat_id)
    context.job_queue.run_repeating(evento_vid, interval=VID_WAIT_TIME, first=1, context=update.message.chat_id)
    context.job_queue.run_repeating(evento_sum, interval=VID_SUMMARY_TIME, first=1, context=update.message.chat_id)
    user = update.effective_user
    wellcome_msg = """
    Hi, [%s](tg://user?id=%s)\! 🕊️ \nWe are starting monitoring
    """ % (user.first_name, str(user.id))
    # Buttons
    actions_keyboard = [[KeyboardButton(START_MONITORING), KeyboardButton(STOP_MONITORING)], [KeyboardButton(CAPTURE_IMAGE)], [KeyboardButton(RECORD_VIDEO)]]

    context.bot.send_chat_action(update.message.chat_id, action=ChatAction.TYPING, timeout=3)
    context.bot.send_message(chat_id=update.message.chat_id, text=wellcome_msg, parse_mode='MarkdownV2')
    update.message.reply_text(text='Select an option: 🕊️', reply_markup=ReplyKeyboardMarkup(actions_keyboard))


def capture(update: Update, context: CallbackContext) -> None:
    # Validation to work only in groups
    if not is_called_on_group(update):
        return
    context.bot.send_chat_action(update.message.chat_id, action=ChatAction.UPLOAD_PHOTO, timeout=IMG_WAIT_TIME)
    try:
        record_thread = threading.Thread(target=take_a_picture)
        record_thread.start()
    except Exception as e:
        print('An error occurred when the picture was being taken!: ' + str(e))
        # pass


def record(update: Update, context: CallbackContext) -> None:
    # Validation to work only in groups
    if not is_called_on_group(update):
        return
    context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.RECORD_VIDEO, timeout=RECORD_TIME)
    try:
        record_thread = threading.Thread(target=record_a_video, args=(RECORD_TIME,))
        record_thread.start()
    except Exception as e:
        print('An error occurred when the video was being recorded!: ' + str(e))
        # pass


def finish(update: Update, context: CallbackContext) -> None:
    # Validation to work only in groups
    if not is_called_on_group(update):
        return
    update.message.reply_text('Monitoring has stopped!')
    # context.job_queue.stop()
    os.kill(os.getpid(), signal.SIGINT)


def pause(update: Update, context: CallbackContext) -> None:
    # Validation to work only in groups
    if not is_called_on_group(update):
        return
    intervalo = int(update.message.text.replace('/pause_', ''))
    print(intervalo, type(intervalo))
    if not intervalo:
        intervalo = 10
    update.message.reply_text('Pausa!' + str(intervalo))
    context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING, timeout=1)
    time.sleep(intervalo)


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    # Validation to work only in groups
    if not is_called_on_group(update):
        return
    # Preparamos el texto que queremos enviar
    context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING, timeout=3)
    bot_msg = "Comandos disponibles:\n" \
              "- /start\n" \
              "- /capture\n" \
              "- /record\n" \
              "- /finish\n" \
              "- /help\n"
    # Respondemos al mensaje recibido (aqui no hace falta determinar cual es el ID del chat, ya que 
    # "update" contiene dicha informacion y lo que vamos es a responder)
    update.message.reply_text(bot_msg)


def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    # Validation to work only in groups
    if not is_called_on_group(update):
        return
    update.message.reply_text(update.message.text)


def message_handler(update: Update, context: CallbackContext):
    # Validation to work only in groups
    if not is_called_on_group(update):
        return
    if START_MONITORING in update.message.text:
        start(update, context)
    elif STOP_MONITORING in update.message.text:
        finish(update, context)
    elif CAPTURE_IMAGE in update.message.text:
        capture(update, context)
    elif RECORD_VIDEO in update.message.text:
        record(update, context)
    else:
        context.bot.send_message(chat_id=update.message.chat_id, text="I don't understand, better try one of the menu options 👀")


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN)

    # Create bot menu button, to show avalible commands
    bot = Bot(TOKEN)
    commands = [BotCommand("start", "to start bot monitoring"), BotCommand("stop", "to stop bot monitoring")]
    bot.set_my_commands(commands)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("stop", finish))
    dispatcher.add_handler(MessageHandler(Filters.text, message_handler))
    # dispatcher.add_handler(CommandHandler("capture", capture))
    # dispatcher.add_handler(CommandHandler("record", record))
    # dispatcher.add_handler(CommandHandler("help", help_command))

    # dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))  # Replica lo que recibe

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
