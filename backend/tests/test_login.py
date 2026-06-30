# tests/test_auth.py
from datetime import datetime, timezone, timedelta
from typing import Generator
import pytest
from jose import jwt, ExpiredSignatureError
from sqlalchemy.orm import Session
from app.api.services.login import authenticate_user, create_access_token
from app.api.services.users import create_user
from app.api.schemas.users import UserCreate
import os

SECRET_KEY = os.getenv("SECRET_KEY", "testsecret")  # fallback pour tests
ALGORITHM = "HS256"

# Generation of a unique user
def unique_user(username_prefix: str) -> UserCreate:
    """Génère un UserCreate unique pour éviter les collisions."""
    timestamp = int(datetime.now(timezone.utc).timestamp() * 1000)
    return UserCreate(
        username=f"{username_prefix}_{timestamp}",
        email=f"{username_prefix}_{timestamp}@example.com",
        password="password123"
    )

# Creation of a DB session for the tests
@pytest.fixture
def db_session(test_db) -> Generator[Session, None, None]:
    db = test_db()
    try:
        yield db
    finally:
        db.close()

# Autentication test
def test_authenticate_user_success(db_session):
    user_in = unique_user("alice")
    user = create_user(db_session, user_in)

    authenticated_user = authenticate_user(db_session, user.username, "password123")
    assert authenticated_user is not None
    assert authenticated_user.id == user.id

def test_authenticate_user_wrong_password(db_session):
    user_in = unique_user("bob")
    user = create_user(db_session, user_in)

    authenticated_user = authenticate_user(db_session, user.username, "wrongpassword")
    assert authenticated_user is None

def test_authenticate_user_not_found(db_session):
    authenticated_user = authenticate_user(db_session, "nonexistent_user", "password123")
    assert authenticated_user is None

def test_create_access_token_contains_user_id():
    user_id = 42
    token = create_access_token(user_id)
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert payload["sub"] == str(user_id)
    assert datetime.fromtimestamp(payload["exp"], tz=timezone.utc) > datetime.now(timezone.utc)

def test_create_access_token_expired():
    user_id = 42
    token = create_access_token(user_id, expires_delta=timedelta(seconds=-10))
    with pytest.raises(ExpiredSignatureError):
        jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])