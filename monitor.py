import time
import logging
import asyncio
from utils import (
    send_telegram_message,
    get_current_price,
    calculate_percent_change,
    should_alert,
    format_alert_message
)
from config import (
    SYMBOL,
    ALERT_PERCENT
)

logging.info("Скрипт процентного мониторинга Bybit запущен...")

try:
    base_price = get_current_price()
    logging.info("Начальная базовая цена {} зафиксирована: {} USD".format(SYMBOL, base_price))
except Exception as exc:
    logging.critical("Не удалось получить начальную цену: {}".format(exc))
    exit(1)

try:
    while True:
        try:
            current_price = get_current_price()
            percent_change = calculate_percent_change(current_price, base_price)

            logging.info("Цена: {} USD | Изменение: {:+.2f}% (База: {})".format(current_price, percent_change, base_price))

            if should_alert(percent_change, ALERT_PERCENT):
                message = format_alert_message(SYMBOL, percent_change, current_price, base_price)

                asyncio.run(send_telegram_message(message))
                logging.info("Отправлено уведомление в Telegram. Изменение: {:+.2f}%".format(percent_change))

                base_price = current_price
                logging.info("Базовая цена обновлена до: {} USD".format(base_price))

        except Exception as exc:
            logging.error("Произошла ошибка при выполнении: {}".format(exc))

        time.sleep(7)

except KeyboardInterrupt:
    exit(1)