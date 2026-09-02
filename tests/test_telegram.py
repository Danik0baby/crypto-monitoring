from unittest import mock

import aiohttp
import pytest

from utils import send_telegram_message


class _FakeResponse:
    """Имитация aiohttp.ClientResponse."""

    def __init__(self, status=200, text="ok"):
        self.status = status
        self._text = text

    async def text(self):
        return self._text


class _FakePostContext:
    """Контекстный менеджер для client.post(...) из aiohttp."""

    def __init__(self, response):
        self._response = response

    async def __aenter__(self):
        return self._response

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        return False


class _FakeClientSession:
    """Имитация aiohttp.ClientSession, запоминающая вызовы post()."""

    def __init__(self, response):
        self._response = response
        self.calls = []

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        return False

    def post(self, url, **kwargs):
        self.calls.append((url, kwargs))
        return _FakePostContext(self._response)


@pytest.mark.asyncio
async def test_send_telegram_message_success():
    fake = _FakeClientSession(_FakeResponse(status=200))

    with mock.patch("utils.aiohttp.ClientSession", return_value=fake):
        await send_telegram_message("test message", token="tok", chat_id="chat")

    assert len(fake.calls) == 1
    url, kwargs = fake.calls[0]
    assert url == "https://api.telegram.org/bottok/sendMessage"
    assert kwargs == {"json": {"chat_id": "chat", "text": "test message"}}


@pytest.mark.asyncio
async def test_send_telegram_message_non_200_does_not_raise():
    """При ответе Telegram с ошибкой функция не должна бросать исключение."""
    fake = _FakeClientSession(_FakeResponse(status=500, text="internal error"))

    with mock.patch("utils.aiohttp.ClientSession", return_value=fake):
        await send_telegram_message("hello", token="tok", chat_id="chat")

    assert len(fake.calls) == 1


@pytest.mark.asyncio
async def test_send_telegram_message_network_error_does_not_raise():
    """Сбой сети не должен останавливать мониторинг."""
    fake = _FakeClientSession(_FakeResponse(status=200))
    fake.post = mock.Mock(side_effect=aiohttp.ClientConnectionError("down"))

    with mock.patch("utils.aiohttp.ClientSession", return_value=fake):
        await send_telegram_message("hello", token="tok", chat_id="chat")