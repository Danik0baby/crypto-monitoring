import requests
import logging
import aiohttp
import asyncio
from pybit.unified_trading import HTTP
from config import (
    TELEGRAM_TOKEN,
    CHAT_ID,
    SYMBOL,
    ALERT_PERCENT
)

session = HTTP(testnet=False)

async def send_telegram_message(text):
    url = "https://api.telegram.org/bot{}/sendMessage".format(TELEGRAM_TOKEN)
    payload = {"chat_id": CHAT_ID, "text": text}
    try:
        async with aiohttp.ClientSession() as client:
            async with client.post(url, json=payload) as response:
                if response.status_code != 200:
                    error = await response.text()
                    logging.error("Ошибка отправки в Telegram: {}".format(response.text))
    except Exception as err:
        logging.error("Ошибка сети при отправке в Telegram: {}".format(err))
        
        
def get_current_price():
    response = session.get_tickers(category="linear", symbol=SYMBOL)
    return float(response['result']['list'][0]['lastPrice'])