from fastapi import Depends, HTTPException, status, Cookie
from jose import jwt
import os
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.api.services.users import get_user_by_id

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"


# Extract the information of the current user from the cookie
def get_current_user(
    db: Session = Depends(get_db),
    access_token: str = Cookie(None)
):
    if not access_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Not authenticated")
    try:
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = int(payload.get("sub"))
        user = get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="User not found")
        return user
    except jwt.JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid token")