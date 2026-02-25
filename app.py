import os
import requests
from bs4 import BeautifulSoup
import telegram
import time

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

URL = "https://molodyytheatre.com/tickets/5515"

bot = telegram.Bot(token=BOT_TOKEN)
known_dates = set()

def get_dates():
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, "html.parser")
    dates = set()

    for el in soup.find_all("div"):
        text = el.get_text(strip=True)
        if "2026" in text:
            dates.add(text)

    return dates

def send_message(text):
    bot.send_message(chat_id=CHAT_ID, text=text)

while True:
    try:
        current_dates = get_dates()
        new_dates = current_dates - known_dates

        if new_dates:
            for date in new_dates:
                send_message(f"🔥 Нова дата Кабара:\n{date}")

        known_dates.update(current_dates)

    except Exception as e:
        send_message(f"⚠️ Помилка: {e}")

    time.sleep(1800)
