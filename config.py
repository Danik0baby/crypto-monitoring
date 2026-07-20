import requests
import os
import logging
from dotenv import load_dotenv
from pybit.unified_trading import HTTP

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("app.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
SYMBOL = os.getenv("SYMBOL")
ALERT_PERCENT = float(os.getenv("ALERT_PERCENT", 1.0))

if not TELEGRAM_TOKEN or not CHAT_ID:
    logging.critical("Ошибка: TELEGRAM_TOKEN или CHAT_ID не найдены в файле .env!")
    exit(1)

session = HTTP(testnet=False)

def send_telegram_message(text):
    url = "https://api.telegram.org/bot{}/sendMessage".format(TELEGRAM_TOKEN)
    payload = {"chat_id": CHAT_ID, "text": text}
    try:
        response = requests.post(url, json=payload)
        if response.status_code != 200:
            logging.error("Ошибка отправки в Telegram: {}".format(response.text))
    except Exception as err:
        logging.error("Ошибка сети при отправке в Telegram: {}".format(err))

def get_current_price():
    response = session.get_tickers(category="linear", symbol=SYMBOL)
    return float(response['result']['list'][0]['lastPrice'])
