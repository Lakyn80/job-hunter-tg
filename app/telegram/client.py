import os
from telethon import TelegramClient, events
from dotenv import load_dotenv

from app.db.database import SessionLocal
from app.db.repository import job_exists, save_job

load_dotenv()

API_ID = int(os.getenv("TELEGRAM_API_ID"))
API_HASH = os.getenv("TELEGRAM_API_HASH")
SESSION = os.getenv("TELEGRAM_SESSION", "job_hunter")

client = TelegramClient(SESSION, API_ID, API_HASH)


# ---- kompatibilita pro testy ----
def get_client():
    return client
# ---------------------------------


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


async def connect_client():
    await client.start()
    print("✅ Telegram client přihlášen")

    for dialog in await client.get_dialogs():
        if dialog.name == "Python_Jbs":
            print("📜 Načítám posledních 50 zpráv z @Python_Jbs")
            async for msg in client.iter_messages(dialog, limit=50):
                if not msg.text:
                    continue

                text = msg.text.strip()

                if not is_relevant_job(text):
                    continue

                channel = dialog.entity.username or str(dialog.entity.id)
                message_id = msg.id
                title = text.splitlines()[0][:500]

                db = SessionLocal()
                try:
                    if job_exists(db, channel, message_id):
                        continue

                    save_job(
                        db=db,
                        channel=channel,
                        message_id=message_id,
                        title=title,
                        text_original=text,
                    )
                finally:
                    db.close()


async def disconnect_client():
    await client.disconnect()
