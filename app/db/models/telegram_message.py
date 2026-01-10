from sqlalchemy import Column, Integer, String, Text, DateTime, UniqueConstraint
from datetime import datetime

from app.db.database import Base


class TelegramMessage(Base):
    __tablename__ = "telegram_messages"

    id = Column(Integer, primary_key=True, index=True)

    channel = Column(String(255), index=True, nullable=False)
    message_id = Column(Integer, nullable=False)

    original_text = Column(Text, nullable=False)
    translated_text = Column(Text, nullable=True)

    language = Column(String(10), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint("channel", "message_id", name="uq_channel_message"),
    )
