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

import os
import signal
import logging
import time
import threading

from telegram import *
from telegram.ext import *
from dotenv import load_dotenv

from tools import *

load_dotenv()

cam_video_url = os.getenv('URL_CAM1')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

TOKEN   = os.getenv('BOT_TELEGRAM_TOKEN')
img_str       = None
video_str     = None
path_img      = "images/event.jpg"
path_video    = "videos/event.mp4"
IMG_WAIT_TIME = 3
VID_WAIT_TIME = 5
RECORD_TIME   = 10

# MESSAGES
START_MONITORING = "Start Monitoring"
STOP_MONITORING  = "Stop Monitoring"
CAPTURE_IMAGE    = "Capture Image"
RECORD_VIDEO     = "Record Video"

# Define a few command handlers. These usually take the two arguments update and
# context.
def read_img():
    # ret, frame = cap.read()
    if os.path.isfile(path_img):
        img_str = open(path_img, "rb")
    else:
        return ""
    return img_str


def read_video():
    # ret, frame = cap.read()
    if os.path.isfile(path_video):
        video_str = open(path_video, "rb")
    else:
        return ""
    return video_str


def evento_img(context):
    chat_id = context.job.context
    binario = ""
    binario = read_img()
    if binario == "":
        print("No events.")
    else:
        # if required_time_is_completed(path_video, IMG_WAIT_TIME):
        context.bot.send_chat_action(chat_id, action=ChatAction.UPLOAD_PHOTO, timeout=IMG_WAIT_TIME)
        context.bot.send_photo(chat_id, photo=binario)
        binario.close()
        os.remove(path_img)


def evento_vid(context):
    print("Video event..")
    chat_id = context.job.context
    binario = ""
    binario = read_video()
    if binario == "":
        print("No events.")
        # pass
    else:
        print("Have a video here!")
        if required_time_is_completed(path_video, VID_WAIT_TIME):
            video_duration(path_video)
            print("Its time to send the video!")
            video_size = get_file_size_in_mb(path_video)
            print("Size: " + str(video_size))
            if video_size >= 20:
                # context.bot.send_document(chat_id, document=binario)
                context.bot.send_chat_action(chat_id, action=ChatAction.TYPING, timeout=RECORD_TIME)
                context.bot.send_message(chat_id, text="The video is too long, I can't send it, sorry 🙁")
            else:
                context.bot.send_chat_action(chat_id, action=ChatAction.UPLOAD_VIDEO, timeout=RECORD_TIME)
                context.bot.send_video(chat_id, video=binario, supports_streaming=True)
            binario.close()
            os.remove(path_video)
    

def shutdown():
    Updater.stop()
    Updater.is_idle = False


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    context.job_queue.run_repeating(evento_img, interval=IMG_WAIT_TIME, first=1, context=update.message.chat_id)
    context.job_queue.run_repeating(evento_vid, interval=VID_WAIT_TIME, first=1, context=update.message.chat_id)
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
    context.bot.send_chat_action(update.message.chat_id, action=ChatAction.UPLOAD_PHOTO, timeout=IMG_WAIT_TIME)
    try:
        record_thread = threading.Thread(target=take_a_picture)
        record_thread.start()
    except Exception as e:
        print('An error occurred when the picture was being taken!: ' + str(e))
        # pass


def record(update: Update, context: CallbackContext) -> None:
    context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.RECORD_VIDEO, timeout=RECORD_TIME)
    try:
        record_thread = threading.Thread(target=record_a_video, args=(RECORD_TIME,))
        record_thread.start()
    except Exception as e:
        print('An error occurred when the video was being recorded!: ' + str(e))
        # pass


def finish(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Monitoring has stopped!')
    # context.job_queue.stop()
    os.kill(os.getpid(), signal.SIGINT)


def pause(update: Update, context: CallbackContext) -> None:
    intervalo = int(update.message.text.replace('/pause_', ''))
    print(intervalo, type(intervalo))
    if not intervalo:
        intervalo = 10
    update.message.reply_text('Pausa!' + str(intervalo))
    context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING, timeout=1)
    time.sleep(intervalo)


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
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
    update.message.reply_text(update.message.text)


def message_handler(update: Update, context: CallbackContext):
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

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text, message_handler))
    # dispatcher.add_handler(CommandHandler("capture", capture))
    # dispatcher.add_handler(CommandHandler("record", record))
    # dispatcher.add_handler(CommandHandler("finish", finish))
    # dispatcher.add_handler(CommandHandler("help", help_command))

    # dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))  # Replica lo que recibe

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
