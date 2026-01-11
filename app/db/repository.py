from sqlalchemy.orm import Session
from app.db.models import Job


def job_exists(db: Session, channel: str, message_id: int) -> bool:
    return (
        db.query(Job)
        .filter(Job.channel == channel, Job.message_id == message_id)
        .first()
        is not None
    )


def save_job(
    db: Session,
    channel: str,
    message_id: int,
    title: str | None,
    text_original: str,
):
    job = Job(
        channel=channel,
        message_id=message_id,
        title=title,
        text_original=text_original,
        text_cs=None,
        translate_requested=False,
    )
    db.add(job)
    db.commit()
    db.refresh(job)
    return job


def mark_for_translation(db: Session, job_id: int) -> Job | None:
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        return None

    job.translate_requested = True
    db.commit()
    db.refresh(job)
    return job
