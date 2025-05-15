# utils/telegram_notify.py
import requests

TELEGRAM_BOT_TOKEN = '7375155413:AAEFEaa4Izf0P82cFiFsO9Ws9oviJiBOG8I'
CHAT_ID = '6630985343'

def send_telegram_message(message):
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    data = {
        'chat_id': CHAT_ID,
        'text': message,
        'parse_mode': 'HTML'
    }
    try:
        requests.post(url, data=data)
    except Exception as e:
        print(f"Ошибка при отправке в Telegram: {e}")
        