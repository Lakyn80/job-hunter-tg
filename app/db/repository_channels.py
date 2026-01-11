from sqlalchemy.orm import Session
from app.db.models import Channel


def list_channels(db: Session):
    return db.query(Channel).order_by(Channel.created_at.desc()).all()


def get_channel_by_username(db: Session, tg_username: str):
    return db.query(Channel).filter(Channel.tg_username == tg_username).first()


def create_channel(db: Session, tg_username: str):
    channel = Channel(tg_username=tg_username)
    db.add(channel)
    db.commit()
    db.refresh(channel)
    return channel


def set_channel_enabled(db: Session, channel_id: int, enabled: bool):
    channel = db.query(Channel).filter(Channel.id == channel_id).first()
    if not channel:
        return None

    channel.enabled = enabled
    db.commit()
    db.refresh(channel)
    return channel
