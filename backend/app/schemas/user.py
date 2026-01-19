"""
User schemas
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    """Base user schema"""
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    full_name: Optional[str] = None


class UserCreate(UserBase):
    """User creation schema"""
    password: str = Field(..., min_length=6)
    role_id: Optional[int] = None


class UserUpdate(BaseModel):
    """User update schema"""
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    avatar_url: Optional[str] = None
    role_id: Optional[int] = None
    status: Optional[str] = None


class UserPasswordUpdate(BaseModel):
    """User password update schema"""
    old_password: str
    new_password: str = Field(..., min_length=6)


class UserInDB(UserBase):
    """User in database schema"""
    id: int
    avatar_url: Optional[str] = None
    role_id: Optional[int] = None
    status: str
    created_at: datetime
    updated_at: datetime
    last_login_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserResponse(UserInDB):
    """User response schema with role info"""
    role_name: Optional[str] = None
    role_display_name: Optional[str] = None


class Token(BaseModel):
    """Token schema"""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Token data schema"""
    user_id: Optional[int] = None
    username: Optional[str] = None


class LoginRequest(BaseModel):
    """Login request schema"""
    username: str
    password: str
