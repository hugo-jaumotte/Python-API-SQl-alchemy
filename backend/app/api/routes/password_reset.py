from fastapi import APIRouter, Depends, HTTPException
from app.api.services.mailing import send_password_reset_email
from app.api.services.users import get_user_by_email
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.api.schemas.password_reset import ResetPassword, PasswordResetRequest
from app.api.services.password_reset import generate_reset_token, reset_password_token

router = APIRouter(
    prefix="/password-reset",
    tags=["Password Reset"]
)

# 🔹 Password reset request
@router.post("/request")
def request_password_reset(
    data: PasswordResetRequest,
    db: Session = Depends(get_db)
):
    user = get_user_by_email(db, data.email)

    if user:
        token = generate_reset_token(user.id)
        send_password_reset_email(user.email, token)

    # Same response whether the email exists or not to prevent user enumeration
    return {"detail": "If an account exists, an email has been sent"}


@router.post("/confirm")
def confirm_password_reset(
    data: ResetPassword,
    db: Session = Depends(get_db)
):
    reset_password_token(
        token=data.token,
        new_password=data.new_password,
        db=db
    )

    return {"detail": "Password reset successful"}