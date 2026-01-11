from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import Job
from app.services.translator import translate_to_cs

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.post("/{job_id}/translate")
async def translate_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    if job.text_cs:
        return {
            "id": job.id,
            "status": "already_translated",
        }

    translated = await translate_to_cs(job.text_original)

    job.text_cs = translated
    job.translate_requested = False
    db.commit()
    db.refresh(job)

    return {
        "id": job.id,
        "status": "translated",
    }
