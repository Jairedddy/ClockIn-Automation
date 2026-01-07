import requests
import os

def send_telegram_message(bot_token, chat_id, text):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    }
    requests.post(url, json=payload, timeout=10)
    
def send_telegram_photo(bot_token, chat_id, photo_path, caption=None):
    url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"
    
    with open(photo_path, "rb") as photo:
        files = {"photo": photo}
        data = {
            "chat_id": chat_id,
            "caption": caption or ""
        }
        requests.post(url, data=data, files=files, timeout = 20)