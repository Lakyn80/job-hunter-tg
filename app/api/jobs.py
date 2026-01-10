from fastapi import APIRouter, Query
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.db.models import TelegramMessage

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.get("/")
def list_jobs(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    db: Session = SessionLocal()
    try:
        items = (
            db.query(TelegramMessage)
            .filter(TelegramMessage.is_job == True)
            .order_by(TelegramMessage.created_at.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )

        return [
            {
                "telegram_id": m.telegram_id,
                "channel": m.channel,
                "text": m.text,
                "created_at": m.created_at,
            }
            for m in items
        ]
    finally:
        db.close()
