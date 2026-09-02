from utils import format_alert_message


def test_format_alert_message_positive_change():
    message = format_alert_message("BTCUSDT", 2.5, 102.5, 100.0)

    assert "BTCUSDT" in message
    assert "Изменение цены: +2.50%" in message
    assert "Текущая цена: 102.5 USD" in message
    assert "Предыдущая база: 100.0 USD" in message
    assert message.startswith("Внимание! Мониторинг BTCUSDT")


def test_format_alert_message_negative_change():
    message = format_alert_message("ETHUSDT", -3.25, 966.75, 1000.0)

    assert "ETHUSDT" in message
    assert "Изменение цены: -3.25%" in message
    assert "Текущая цена: 966.75 USD" in message
    assert "Предыдущая база: 1000.0 USD" in message


def test_format_alert_message_contains_newlines():
    """Сообщение должно быть многострочным, удобным для чтения в мессенджере."""
    message = format_alert_message("SOLUSDT", 1.0, 101.0, 100.0)
    assert message.count("\n") == 3