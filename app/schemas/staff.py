import uuid
from pydantic import BaseModel, EmailStr, Field

class StaffCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    full_name: str = Field(min_length=2, max_length=120)
    specialization: str = Field(min_length=2, max_length=100)
    bio: str | None = None

class StaffProfileResponse(BaseModel):
    id: uuid.UUID
    specialization: str
    bio: str | None
    
    model_config = {"from_attributes": True}