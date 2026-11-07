import uuid
from pydantic import BaseModel, EmailStr, Field
from app.models.user import UserRole

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    full_name: str = Field(min_length=2, max_length=120)

class UserResponse(BaseModel):
    id: uuid.UUID
    email: EmailStr
    full_name: str
    role: UserRole

    model_config = {"from_attributes": True}