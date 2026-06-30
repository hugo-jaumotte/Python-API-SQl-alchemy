from datetime import datetime
from pydantic import BaseModel, ConfigDict
from pydantic import EmailStr

#Pydantic models for creating and outputting User data
class UserCreate(BaseModel):
    username: str
    password: str
    email: EmailStr

class UserOut(BaseModel):
    username: str
    email: EmailStr
    is_verified: bool

    model_config = ConfigDict(from_attributes=True)