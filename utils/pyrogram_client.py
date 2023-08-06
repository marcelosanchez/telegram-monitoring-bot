from pyrogram import enums
import traceback


def send_message(file_path, file_type, client, chat_id, caption):
    """
    Send a message to a Telegram chat, along with a file if applicable.
    """
    try:
        # Determine the appropriate method based on the file_type
        send_method = {
            'video': client.send_video,
            'photo': client.send_photo
        }.get(file_type)

        if send_method:
            send_method(
                chat_id=chat_id,
                caption=caption,
                parse_mode=enums.ParseMode.MARKDOWN,
                ** {file_type: file_path}  # use dict to unpack arguments
            )

    except Exception as error_msg:
        error_traceback = traceback.format_exc()
        print("send_message | error: ", str(error_msg), "\n", error_traceback)
        send_error_msg(client, chat_id, str(error_msg))


def send_error_msg(client, chat_id, error_msg):
    """
    Send an error message to a Telegram chat.

    Args:
        client (pyrogram.Client): The Pyrogram client object.
        chat_id (str): The chat_id of the recipient chat.
        error_msg (str): The error message to be sent.
    """
    # T0D0: Create a bot for handling logs
    prefix = "⚠️ Ops something went wrong: "
    message = prefix + error_msg
    client.send_message(
        chat_id=chat_id,
        text=message,
    )
