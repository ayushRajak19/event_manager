"""
Item request schemas - Request and response models.
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class ItemRequestCreate(BaseModel):
    """Create item request schema."""
    item_name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    category: Optional[str] = Field(None, max_length=100)


class ItemRequestResponse(BaseModel):
    """Item request response schema."""
    id: int
    user_id: int
    item_name: str
    description: Optional[str]
    category: Optional[str]
    status: str
    vendor_id: Optional[int]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ItemRequestDetailResponse(ItemRequestResponse):
    """Detailed item request response with user and vendor info."""
    user: Optional[dict] = None
    vendor: Optional[dict] = None


class ItemRequestStatusUpdate(BaseModel):
    """Update item request status schema."""
    status: str
    vendor_id: Optional[int] = None


class ItemRequestListResponse(BaseModel):
    """Item request list response with pagination."""
    total: int
    page: int
    page_size: int
    items: List[ItemRequestResponse]
