"""
Product schemas - Request and response models.
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ProductCreate(BaseModel):
    """Create product request schema."""
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    category: Optional[str] = Field(None, max_length=100)
    quantity: int = Field(..., ge=0)
    price: float = Field(..., gt=0)
    status: Optional[str] = "available"


class ProductUpdate(BaseModel):
    """Update product request schema."""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    category: Optional[str] = Field(None, max_length=100)
    quantity: Optional[int] = Field(None, ge=0)
    price: Optional[float] = Field(None, gt=0)
    status: Optional[str] = None


class ProductResponse(BaseModel):
    """Product response schema."""
    id: int
    name: str
    description: Optional[str]
    category: Optional[str]
    quantity: int
    price: float
    status: str
    vendor_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ProductDetailResponse(ProductResponse):
    """Detailed product response with vendor info."""
    vendor: Optional[dict] = None
