import requests
from django.conf import settings


def send_telegram_message(chat_id, message):
    url = (
        f'https://api.telegram.org/bot'
        f'{settings.TELEGRAM_BOT_TOKEN}/sendMessage'
    )

    data = {
        'chat_id': chat_id,
        'text': message,
    }

    response = requests.post(
        url,
        data=data,
        timeout=10,
    )

    response.raise_for_status()

    return response.json()
