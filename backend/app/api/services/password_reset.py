from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.db.models import Token, User
from passlib.context import CryptContext
from jose import jwt, JWTError
import os

SECRET_KEY = os.getenv("SECRET_KEY", "dev_secret")
ALGORITHM = "HS256"

# Generate the token that contain the id of the user that will change their password
def generate_reset_token(user_id: int, expires_minutes: int = 15) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)

    payload = {
        "sub": str(user_id),
        "type": "reset_password",
        "exp": expire
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Replace the password of the user with the id in argument by the new password in argument
def reset_password_token(token: str, new_password: str, db: Session):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        if payload.get("type") != "reset_password":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid token type"
            )

        user_id = payload.get("sub")

        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid token payload"
            )

        user = db.query(User).filter(User.id == int(user_id)).first()

        if not user:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

        user.hashed_password = pwd_context.hash(new_password)
        db.commit()

        return {
            "message": "Password reset successfully"
        }

    except JWTError:
        raise HTTPException(
            status_code=400,
            detail="Invalid or expired token"
        )