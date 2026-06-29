import requests

from django.conf import settings


class TelegramBot:

    BASE_URL = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}"

    @classmethod
    def send_message(cls, chat_id: int, text: str):

        url = f"{cls.BASE_URL}/sendMessage"

        payload = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "HTML",
            "disable_web_page_preview": True,
        }

        response = requests.post(
            url,
            json=payload,
            timeout=15,
        )

        response.raise_for_status()