from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50, description="User's full name")
    email: EmailStr = Field(..., description="User's email address")
    
class UserCreate(UserBase):
    role: Optional[str] = Field("user", description="User role (admin or user)")
    
class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=50, description="User's full name")
    role: Optional[str] = Field(None, description="User role (admin or user)")

class UserResponse(UserBase):
    id: int
    role: str
    created_at: datetime
    
    class Config:
        orm_mode = True