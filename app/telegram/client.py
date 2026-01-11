# -*- coding: utf-8 -*-

import os
from telethon import TelegramClient

_client: TelegramClient | None = None


def get_client() -> TelegramClient:
    """
    Lazily create and return Telegram client.
    Environment variables are read ONLY when this function is called.
    This keeps unit tests and CI isolated from Telegram credentials.
    """
    global _client

    if _client is not None:
        return _client

    api_id_raw = os.getenv("TELEGRAM_API_ID")
    api_hash = os.getenv("TELEGRAM_API_HASH")
    session_name = os.getenv("TELEGRAM_SESSION", "job_hunter")

    if not api_id_raw or not api_hash:
        raise RuntimeError("Telegram credentials are not configured")

    api_id = int(api_id_raw)

    _client = TelegramClient(session_name, api_id, api_hash)
    return _client


async def connect_client():
    try:
        client = get_client()
        await client.start()
        print("Telegram client connected")
    except RuntimeError:
        # Expected in tests / CI
        print("Telegram client disabled (no credentials)")


async def disconnect_client():
    global _client
    if _client:
        await _client.disconnect()
        _client = None
