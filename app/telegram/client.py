import os
from telethon import TelegramClient, events
from dotenv import load_dotenv

from app.db.database import SessionLocal
from app.db.repository import job_exists, save_job

load_dotenv()

client = None


def get_client():
    return client


ALLOWED_SENIORITY = [
    "junior", "jun", "middle", "mid", "младший", "начальный"
]

FORBIDDEN_SENIORITY = [
    "senior", "lead", "team lead", "architect", "principal", "expert", "старший"
]

ALLOWED_TECH = [
    "python", "flask", "fastapi", "sql", "postgres", "sqlite",
    "docker", "rest", "api", "pandas", "react", "javascript", "js", "git"
]


def is_relevant_job(text: str) -> bool:
    t = text.lower()

    if any(x in t for x in FORBIDDEN_SENIORITY):
        return False

    if not any(x in t for x in ALLOWED_SENIORITY):
        return False

    if not any(x in t for x in ALLOWED_TECH):
        return False

    return True


async def connect_client():
    global client

    api_id = os.getenv("TELEGRAM_API_ID")
    api_hash = os.getenv("TELEGRAM_API_HASH")
    session = os.getenv("TELEGRAM_SESSION", "job_hunter")

    if not api_id or not api_hash:
        raise RuntimeError("Missing TELEGRAM_API_ID or TELEGRAM_API_HASH")

    client = TelegramClient(session, int(api_id), api_hash)

    @client.on(events.NewMessage)
    async def handler(event):
        if not event.text:
            return

        text = event.text.strip()

        if not is_relevant_job(text):
            return

        channel = event.chat.username or str(event.chat_id)
        message_id = event.id
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

    await client.start()
    print("✅ Telegram client přihlášen")


async def disconnect_client():
    if client:
        await client.disconnect()
