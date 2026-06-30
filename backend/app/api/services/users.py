from sqlalchemy.orm import Session
from app.db.models import User
from app.api.schemas.users import UserCreate
from passlib.context import CryptContext
from fastapi import HTTPException
from datetime import datetime, timedelta, timezone
from jose import jwt
import os

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_id(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user

def get_user_by_username(db: Session, username: str):
    user = db.query(User).filter(User.username == username).first()

    return user

def get_user_by_email(db: Session, email: str):
    user = db.query(User).filter(User.email == email).first()

    return user

def create_user(db: Session, user: UserCreate):
    hashed_password = pwd_context.hash(user.password)

    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        is_verified=False
    )

    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error creating user")
    


SECRET_KEY = os.getenv("SECRET_KEY", "dev_secret")
ALGORITHM = "HS256"
EXPIRE_MINUTES = 60 * 24  # 24h

# Generate the token used for the email verification
def create_verification_token(user_id: int):
    payload = {
        "sub": str(user_id),
        "type": "email_verification",
        "exp": datetime.now(timezone.utc) + timedelta(minutes=EXPIRE_MINUTES)
    }

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)