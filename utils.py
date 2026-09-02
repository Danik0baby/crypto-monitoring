import logging
import aiohttp
from pybit.unified_trading import HTTP
from config import (
    TELEGRAM_TOKEN,
    CHAT_ID,
    SYMBOL
)

session = HTTP(testnet=False)


def calculate_percent_change(current_price, base_price):
    """
    Вычисляет процент изменения цены относительно базовой.

    Формула: ((текущая - баз.цена) / баз.цена) * 100

    Raises:
        ValueError: если base_price <= 0.
    """
    if base_price <= 0:
        raise ValueError("base_price должен быть положительным числом")
    return ((current_price - base_price) / base_price) * 100


def should_alert(percent_change, threshold):
    """
    Определяет, достигло ли изменение цены порога срабатывания.

    Срабатывает при abs(percent_change) >= threshold (включая граничное значение).
    """
    return abs(percent_change) >= threshold


def format_alert_message(symbol, percent_change, current_price, base_price):
    """
    Формирует текст уведомления для Telegram.
    """
    return (
        "Внимание! Мониторинг {}\n"
        "Изменение цены: {:+.2f}%\n"
        "Текущая цена: {} USD\n"
        "Предыдущая база: {} USD"
    ).format(symbol, percent_change, current_price, base_price)


async def send_telegram_message(text, token=None, chat_id=None):
    token = token or TELEGRAM_TOKEN
    chat_id = chat_id or CHAT_ID
    url = "https://api.telegram.org/bot{}/sendMessage".format(token)
    payload = {"chat_id": chat_id, "text": text}
    try:
        async with aiohttp.ClientSession() as client:
            async with client.post(url, json=payload) as response:
                if response.status != 200:
                    error = await response.text()
                    logging.error("Ошибка отправки в Telegram: {}".format(error))
    except Exception as err:
        logging.error("Ошибка сети при отправке в Telegram: {}".format(err))


def get_current_price(symbol=None):
    symbol = symbol or SYMBOL
    response = session.get_tickers(category="linear", symbol=symbol)
    return float(response['result']['list'][0]['lastPrice'])