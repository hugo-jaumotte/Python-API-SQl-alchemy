from pydantic import BaseModel, EmailStr

# Incoming data for password reset
class ResetPassword(BaseModel):
    token: str
    new_password: str

class PasswordResetRequest(BaseModel):
    email: EmailStr