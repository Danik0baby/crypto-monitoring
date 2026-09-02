import pytest

import config


def test_alert_percent_is_float():
    assert isinstance(config.ALERT_PERCENT, float)


def test_alert_percent_default_value():
    assert config.ALERT_PERCENT == pytest.approx(1.0)


def test_symbol_from_env():
    assert config.SYMBOL == "BTCUSDT"


def test_telegram_token_from_env():
    assert config.TELEGRAM_TOKEN == "test_token"


def test_chat_id_from_env():
    assert config.CHAT_ID == "123456789"