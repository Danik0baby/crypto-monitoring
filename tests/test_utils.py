from unittest import mock

import pytest

from utils import get_current_price


def _api_response(price):
    return {"result": {"list": [{"lastPrice": str(price)}]}}


def test_get_current_price_success():
    with mock.patch("utils.session") as fake_session:
        fake_session.get_tickers.return_value = _api_response("65432.5")

        result = get_current_price("BTCUSDT")

    assert result == pytest.approx(65432.5)
    fake_session.get_tickers.assert_called_once_with(
        category="linear", symbol="BTCUSDT"
    )


def test_get_current_price_uses_default_symbol_from_config():
    with mock.patch("utils.session") as fake_session:
        fake_session.get_tickers.return_value = _api_response("100.0")

        result = get_current_price()

    assert result == pytest.approx(100.0)
    fake_session.get_tickers.assert_called_once_with(
        category="linear", symbol="BTCUSDT"
    )


def test_get_current_price_with_empty_list_raises_index_error():
    """Ответ Bybit без элементов списка — невалидный ответ."""
    with mock.patch("utils.session") as fake_session:
        fake_session.get_tickers.return_value = {"result": {"list": []}}

        with pytest.raises(IndexError):
            get_current_price("BTCUSDT")


def test_get_current_price_with_api_error_propagates():
    """Сетевая/API ошибка Bybit должна пробрасываться наверх для обработки в цикле."""
    with mock.patch("utils.session") as fake_session:
        fake_session.get_tickers.side_effect = ConnectionError("API is down")

        with pytest.raises(ConnectionError):
            get_current_price("BTCUSDT")