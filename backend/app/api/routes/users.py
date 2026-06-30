from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.api.dependencies import get_current_user
from app.api.services.mailing import send_verification_email
from app.api.services.users import create_verification_token
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.api.schemas.users import UserCreate, UserOut
from app.api.services import users as users_service

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

# GET all users
@router.get("/me", response_model=UserOut)
def get_me(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return current_user


# POST create a new user
@router.post("/register", response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = users_service.get_user_by_username(db, user.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    existing_email = users_service.get_user_by_email(db, user.email)
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    db_user = users_service.create_user(db, user)

    try:
        token = create_verification_token(db_user.id)
    except Exception as e:
        print("TOKEN ERROR:", e)

    try:
        send_verification_email(db_user.email, token)
    except Exception as e:
        print("EMAIL ERROR:", e)

    return db_user