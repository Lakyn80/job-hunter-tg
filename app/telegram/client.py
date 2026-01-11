# -*- coding: utf-8 -*-

import os
from telethon import TelegramClient, events
from dotenv import load_dotenv

from app.db.database import SessionLocal
from app.db.models import Channel
from app.db.repository import job_exists, save_job

load_dotenv()

API_ID = int(os.getenv("TELEGRAM_API_ID"))
API_HASH = os.getenv("TELEGRAM_API_HASH")
SESSION = os.getenv("TELEGRAM_SESSION", "job_hunter")

client = None


def get_enabled_channels():
    db = SessionLocal()
    try:
        channels = (
            db.query(Channel)
            .filter(Channel.enabled == True)
            .all()
        )
        return [c.tg_username for c in channels]
    finally:
        db.close()


async def connect_client():
    global client

    if client:
        return client

    client = TelegramClient(SESSION, API_ID, API_HASH)
    await client.start()
    print("Telegram client connected")

    channels = get_enabled_channels()
    if not channels:
        print("No channels found in DB ? Telegram listener is idle")
        return client

    print(f"Listening to {len(channels)} channels:")
    for ch in channels:
        print(f" - {ch}")

    @client.on(events.NewMessage(chats=channels))
    async def handler(event):
        text = event.message.message
        if not text:
            return

        channel = event.chat.username or str(event.chat_id)
        message_id = event.message.id
        title = text.splitlines()[0][:500]

        db = SessionLocal()
        try:
            if job_exists(db, channel, message_id):
                return

            save_job(
                db=db,
                channel=channel,
                message_id=message_id,
                title=title,
                text_original=text,
            )
        finally:
            db.close()

    return client


async def disconnect_client():
    global client
    if client:
        await client.disconnect()
        client = None
        print("Telegram client disconnected")
