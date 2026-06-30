from fastapi import APIRouter, Depends, Response, status, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.api.schemas.login import UserLogin
from app.api.services.login import authenticate_user, create_access_token, verify_email_token

router = APIRouter(prefix="/auth", tags=["Authentication"])

# POST : login route
@router.post("/login")
def login(user: UserLogin, response: Response, db: Session = Depends(get_db)):
    db_user = authenticate_user(db, user.username, user.password)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username or password")
    if not db_user.is_verified:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Email not verified")

    token = create_access_token(db_user.id)

    # Mettre le token dans un cookie HTTP-only
    response.set_cookie(
        key="access_token",       # nom du cookie
        value=token,
        httponly=True,            # interdit la lecture via JS
        secure=True,              # envoie uniquement sur HTTPS
        samesite="none",           # prévention CSRF simple
        max_age=1800              # expiration en secondes (ici 30 min)
    )

    return {"message": "Login successful"}

# GET : route for the email verification
@router.get("/verify-email")
def verify_email(
    token: str,
    response: Response,
    db: Session = Depends(get_db)
):
    return verify_email_token(token, db, response)

#POST : logout route
@router.post("/logout")
def logout(response: Response):
    response.delete_cookie(
        key="access_token",
        httponly=True,
        secure=True,
        samesite="none",
        path="/"
    )
    return {"message": "logged out"}