from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from datetime import datetime

from app.db.database import Base


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    channel = Column(String(255), index=True)
    message_id = Column(Integer, index=True)
    title = Column(String(500))
    text_original = Column(Text)
    text_cs = Column(Text)

    translate_requested = Column(Boolean, default=False, index=True)

    created_at = Column(DateTime, default=datetime.utcnow)
