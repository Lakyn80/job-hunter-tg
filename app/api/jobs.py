from fastapi import APIRouter, Query, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import Job

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.get("/")
def list_jobs(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    translate_requested: bool | None = None,
    db: Session = Depends(get_db),
):
    q = db.query(Job)

    if translate_requested is not None:
        q = q.filter(Job.translate_requested == translate_requested)

    items = (
        q.order_by(Job.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    return [
        {
            "id": j.id,
            "channel": j.channel,
            "message_id": j.message_id,
            "title": j.title,
            "text_original": j.text_original,
            "text_cs": j.text_cs,
            "translate_requested": j.translate_requested,
            "created_at": j.created_at,
        }
        for j in items
    ]
