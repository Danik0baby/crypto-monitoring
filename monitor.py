import time
import logging
from pybit.unified_trading import HTTP

logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[
            logging.FileHandler("app.log"),
            logging.StreamHandler()
            ]

        )

SYMBOL = "BTCUSDT"

session = HTTP(testnet=False)

logging.info("Запущен")

while True:
    try:
        response = session.get_tickers(category="linear", symbol=SYMBOL)

        price = response['result']['list'][0]['lastPrice']
        logging.info("Цена биткоина " + SYMBOL + " " + price + "USD")

    except Exception as e: 
        logging.error("Ошибка " + e)


    time.sleep(10)
