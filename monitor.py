import os
import time
import logging
import requests
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

logging.info("Скрипт процентного мониторинга Bybit запущен...")

try:
    base_price = get_current_price()
    logging.info("Начальная базовая цена {} зафиксирована: {} USD".format(SYMBOL, base_price))
except Exception as e:
    logging.critical("Не удалось получить начальную цену: {}".format(e))
    exit(1)

while True:
    try:
        current_price = get_current_price()
        percent_change = ((current_price - base_price) / base_price) * 100

        logging.info("Цена: {} USD | Изменение: {:+.2f}% (База: {})".format(current_price, percent_change, base_price))

        if abs(percent_change) >= ALERT_PERCENT:
            message = (
                "Внимание! Мониторинг {}\n"
                "Изменение цены: {:+.2f}%\n"
                "Текущая цена: {} USD\n"
                "Предыдущая база: {} USD"
            ).format(SYMBOL, percent_change, current_price, base_price)

            send_telegram_message(message)
            logging.info("Отправлено уведомление в Telegram. Изменение: {:+.2f}%".format(percent_change))

            base_price = current_price
            logging.info("Базовая цена обновлена до: {} USD".format(base_price))

    except Exception as e: 
        logging.error("Произошла ошибка при выполнении: {}".format(e))

    time.sleep(10)