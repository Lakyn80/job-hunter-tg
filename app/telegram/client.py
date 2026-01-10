# -*- coding: utf-8 -*-

import os
from telethon import TelegramClient, events
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv("TELEGRAM_API_ID"))
API_HASH = os.getenv("TELEGRAM_API_HASH")
SESSION = os.getenv("TELEGRAM_SESSION")
LISTEN_CHANNEL = os.getenv("TELEGRAM_LISTEN_CHANNEL")

_client = None


def get_client() -> TelegramClient:
    global _client
    if _client is None:
        _client = TelegramClient(
            SESSION,
            API_ID,
            API_HASH,
        )
    return _client


async def connect_client() -> None:
    client = get_client()

    await client.connect()

    if not await client.is_user_authorized():
        raise RuntimeError("Telegram session není autorizovaná – spusť login_test.py lokálně")

    print("✅ Telegram client přihlášen (session OK)")

    if not LISTEN_CHANNEL:
        print("⚠️ TELEGRAM_LISTEN_CHANNEL není nastaven")
        return

    print(f"📜 Načítám posledních 50 zpráv z {LISTEN_CHANNEL}")

    async for message in client.iter_messages(LISTEN_CHANNEL, limit=50):
        if message.text:
            print(f"[HIST] {message.date} | {message.text[:300]}")

    @client.on(events.NewMessage(chats=LISTEN_CHANNEL))
    async def handler(event):
        if event.message.text:
            print(f"[NEW] {event.message.date} | {event.message.text[:300]}")


async def disconnect_client() -> None:
    global _client
    if _client:
        await _client.disconnect()
        _client = None
