from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session

from app.api.services import focus_sessions as fs_service
from app.api.schemas.focus_sessions import FocusSessionCreate, FocusSessionOut
from app.db.session import get_db

from app.api.dependencies import get_current_user


from fastapi import Request


router = APIRouter(
    prefix="/focus_sessions",
    tags=["FocusSessions"]
)

# GET /focus_sessions/
@router.get("/", response_model=List[FocusSessionOut])
def get_focus_sessions(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return fs_service.get_focus_sessions(db, current_user.id)


# POST /focus_sessions/
@router.post("/add", response_model=FocusSessionOut)
def create_focus_session(
    session_in: FocusSessionCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return fs_service.create_focus_session(
        db,
        session_in,
        current_user.id
    )