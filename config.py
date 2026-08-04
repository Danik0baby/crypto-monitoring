import os
import logging
from dotenv import load_dotenv

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
    
if not SYMBOL or not ALERT_PERCENT:
    logging.critical("Ошибка: SYMBOL или ALERT_PERCENT не указали в .env файле")
    exit(1)