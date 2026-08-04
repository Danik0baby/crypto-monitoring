import os
import time
import logging
from utils import (
    send_telegram_message,
    get_current_price,
    session
)
from config import (
    TELEGRAM_TOKEN,
    CHAT_ID,
    SYMBOL,
    ALERT_PERCENT
)

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

    time.sleep(7)