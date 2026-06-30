from pydantic import BaseModel

# Incoming data for user login
class UserLogin(BaseModel):
    username: str
    password: str