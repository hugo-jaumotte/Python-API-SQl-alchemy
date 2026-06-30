from typing import Generator
from datetime import datetime, timezone
import pytest
from sqlalchemy.orm import Session

from app.api.services.focus_sessions import (
    create_focus_session,
    get_focus_sessions,
)
from app.api.services.users import create_user
from app.api.schemas.focus_sessions import FocusSessionCreate
from app.api.schemas.users import UserCreate

# Creation of a DB session for the tests
@pytest.fixture
def db_session(test_db) -> Generator[Session, None, None]:
    db = test_db()
    try:
        yield db
    finally:
        db.close()

# Generation of a unique user
def unique_user(username_prefix: str) -> UserCreate:
    timestamp = int(datetime.now(timezone.utc).timestamp() * 1000)

    return UserCreate(
        username=f"{username_prefix}{timestamp}",
        email=f"{username_prefix}{timestamp}@example.com",
        password="pass",
    )

# Creation of a pomodoro session for the specified user
def test_create_focus_session_with_title_only(db_session):
    user_in = unique_user("alice")
    user = create_user(db_session, user_in)

    session_in = FocusSessionCreate(
        work_time=25,
        break_time=5,
        user_id=user.id,
        title="Study",
        start_time=datetime.now(timezone.utc),
    )

    session = create_focus_session(
        db_session,
        session_in,
        user.id,
    )

    assert session.title == "Study"
    assert session.user_id == user.id

# Collect of the user sessions
def test_get_focus_sessions_for_user(db_session):
    user_in = unique_user("kate")
    user = create_user(db_session, user_in)

    before = len(get_focus_sessions(db_session, user_id=user.id))

    session_in = FocusSessionCreate(
        work_time=15,
        break_time=5,
        user_id=user.id,
        title="Quick Session",
        start_time=datetime.now(timezone.utc),
    )

    create_focus_session(
        db_session,
        session_in,
        user.id,
    )

    after = len(get_focus_sessions(db_session, user_id=user.id))

    assert after == before + 1