"""
Authentication schemas - Request and response models.
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class AdminSignup(BaseModel):
    """Admin signup request schema."""
    name: str = Field(..., min_length=1, max_length=255)
    email: EmailStr
    password: str = Field(..., min_length=8)


class AdminLogin(BaseModel):
    """Admin login request schema."""
    email: EmailStr
    password: str


class UserSignup(BaseModel):
    """User signup request schema."""
    name: str = Field(..., min_length=1, max_length=255)
    email: EmailStr
    password: str = Field(..., min_length=8)
    phone: Optional[str] = Field(None, max_length=20)


class UserLogin(BaseModel):
    """User login request schema."""
    email: EmailStr
    password: str


class VendorLogin(BaseModel):
    """Vendor login request schema."""
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """Token response after successful login."""
    access_token: str
    token_type: str = "bearer"
    user_id: int
    email: str
    name: str
    role: str


class UserResponse(BaseModel):
    """User response schema."""
    id: int
    name: str
    email: str
    phone: Optional[str]
    is_active: int
    created_at: datetime

    class Config:
        from_attributes = True


class AdminResponse(BaseModel):
    """Admin response schema."""
    id: int
    name: str
    email: str
    created_at: datetime

    class Config:
        from_attributes = True


class VendorResponse(BaseModel):
    """Vendor response schema."""
    id: int
    name: str
    email: str
    company_name: str
    phone: Optional[str]
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
