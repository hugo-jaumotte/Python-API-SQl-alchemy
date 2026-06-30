from typing import Generator
from datetime import datetime
import pytest
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.api.services.users import create_user
from app.api.schemas.users import UserCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Fixture for the DB session
@pytest.fixture
def db_session(test_db) -> Generator[Session, None, None]:
    db: Session = test_db()
    try:
        yield db
    finally:
        db.rollback()
        db.close()

# Generation of a unique user
def unique_user(username_prefix: str) -> UserCreate:
    timestamp = int(datetime.utcnow().timestamp() * 1000)
    return UserCreate(
        username=f"{username_prefix}_{timestamp}",
        email=f"{username_prefix}_{timestamp}@example.com",
        password="pass"
    )

def test_create_user(db_session):
    user_in = unique_user("alice")
    user = create_user(db_session, user_in)
    assert user.username.startswith("alice_")
    assert user.email.endswith("@example.com")

def test_verify_password(db_session):
    password = "mypassword"
    user_in = unique_user("charlie")
    user_in.password = password
    user = create_user(db_session, user_in)
    
    # Verification with pwd_context
    assert pwd_context.verify(password, user.hashed_password)

    # We verify that a wrong password fail
    assert not pwd_context.verify("wrongpassword", user.hashed_password)