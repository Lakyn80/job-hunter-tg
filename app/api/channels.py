from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.db.repository_channels import (
    list_channels,
    create_channel,
    set_channel_enabled,
    get_channel_by_username,
)

router = APIRouter(prefix="/channels", tags=["channels"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def get_channels(db: Session = Depends(get_db)):
    channels = list_channels(db)
    return [
        {
            "id": c.id,
            "tg_username": c.tg_username,
            "enabled": c.enabled,
            "created_at": c.created_at,
        }
        for c in channels
    ]


@router.post("/")
def add_channel(payload: dict, db: Session = Depends(get_db)):
    tg_username = payload.get("tg_username")
    if not tg_username:
        raise HTTPException(status_code=400, detail="tg_username is required")

    existing = get_channel_by_username(db, tg_username)
    if existing:
        raise HTTPException(status_code=400, detail="Channel already exists")

    channel = create_channel(db, tg_username)
    return {
        "id": channel.id,
        "tg_username": channel.tg_username,
        "enabled": channel.enabled,
    }


@router.patch("/{channel_id}")
def toggle_channel(
    channel_id: int,
    payload: dict,
    db: Session = Depends(get_db),
):
    if "enabled" not in payload:
        raise HTTPException(status_code=400, detail="enabled is required")

    channel = set_channel_enabled(db, channel_id, payload["enabled"])
    if not channel:
        raise HTTPException(status_code=404, detail="Channel not found")

    return {
        "id": channel.id,
        "tg_username": channel.tg_username,
        "enabled": channel.enabled,
    }
