import logging
import os

import pytest

# Устанавливаем обязательные env-переменные ДО импорта config/utils,
# т.к. config.py при их отсутствии вызывает exit(1) прямо при импорте.
# Тесты не должны зависеть от реального .env и ходить в сеть.
os.environ["TELEGRAM_TOKEN"] = "test_token"
os.environ["CHAT_ID"] = "123456789"
os.environ["SYMBOL"] = "BTCUSDT"
os.environ["ALERT_PERCENT"] = "1.0"


@pytest.fixture(autouse=True)
def _quiet_logging():
    """Подавляем лог-вывод в консолю вовремя тестоов."""
    logging.disable(logging.CRITICAL)
    yield
    logging.disable(logging.NOTSET)