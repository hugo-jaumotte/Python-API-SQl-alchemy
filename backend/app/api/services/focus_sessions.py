from sqlalchemy.orm import Session
from datetime import datetime, timezone
from app.db.models import FocusSession
from app.api.schemas.focus_sessions import FocusSessionCreate

# Get all focus sessions from the database for the specified userS
def get_focus_sessions(db: Session, user_id: int):
    return db.query(FocusSession).filter(
        FocusSession.user_id == user_id
    ).all()

# Create a new focus session in the database
def create_focus_session(db: Session, session_in: FocusSessionCreate, user_id: int):
    end_time = datetime.now(timezone.utc)

    db_session = FocusSession(
        start_time=session_in.start_time,
        end_time=end_time,
        work_time=session_in.work_time,
        break_time=session_in.break_time,
        user_id=user_id,
        title=session_in.title
    )

    try:
        db.add(db_session)
        db.commit()
        db.refresh(db_session)
        return db_session

    except Exception:
        db.rollback()
        raise