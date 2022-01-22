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

from telegram import Update, ForceReply, ChatAction
from telegram.ext import Updater, CommandHandler, RegexHandler, MessageHandler, Filters, CallbackContext
from dotenv import load_dotenv

from tools import guardar_captura_camara

load_dotenv()

cam_video_url = os.getenv('URL_CAM1')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

# TOKEN=open('token',"r").read()
TOKEN   = os.getenv('BOT_TELEGRAM_TOKEN')
path    = "images/event.jpg"
img_str = None


# Define a few command handlers. These usually take the two arguments update and
# context.
def read_img():
    # ret, frame = cap.read()
    if os.path.isfile(path):
        img_str = open(path, "rb")
    else:
        return ""
    return img_str


def evento_img(context):
    chat_id=context.job.context
    binario=""
    binario=read_img()
    if binario=="":
        print("Ningun evento.")
    else:
        context.bot.send_photo(chat_id,photo=binario)
        binario.close()
        os.remove(path)
    

def shutdown():
    Updater.stop()
    Updater.is_idle = False


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    tiempo_intevalo = 3
    context.job_queue.run_repeating(evento_img,interval=tiempo_intevalo,first=1,context=update.message.chat_id)
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hola, {user.mention_markdown_v2()}\!',
    )


def capture(update: Update, context: CallbackContext) -> None:
    # guardar_captura()
    guardar_captura_camara()


def finish(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('El monitoreo se ha detenido!')
    # context.job_queue.stop()
    os.kill(os.getpid(), signal.SIGINT)


def pause(update: Update, context: CallbackContext) -> None:
    intervalo = int(update.message.text.replace('/pause_', ''))
    print(intervalo, type(intervalo))
    if not intervalo:
        intervalo = 10
    update.message.reply_text('Pausa!' + str(intervalo))
    context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.RECORD_VIDEO, timeout=1)
    time.sleep(intervalo)


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    # Preparamos el texto que queremos enviar
    bot_msg = "Comandos disponibles:\n" \
              "- /start\n" \
              "- /capture\n" \
              "- /finish\n" \
              "- /help\n"
    # Respondemos al mensaje recibido (aqui no hace falta determinar cual es el ID del chat, ya que 
    # "update" contiene dicha informacion y lo que vamos es a responder)
    update.message.reply_text(bot_msg)


def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("capture", capture))
    dispatcher.add_handler(CommandHandler("finish", finish))
    dispatcher.add_handler(CommandHandler("help", help_command))

    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
