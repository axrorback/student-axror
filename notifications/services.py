from .telegram import TelegramBot
from .templates import new_lesson_message


def notify_new_lesson(lesson):

    chat_id = lesson.group.telegram_chat_id

    if not chat_id:
        return

    TelegramBot.send_message(
        chat_id=chat_id,
        text=new_lesson_message(lesson)
    )