"""
Cart schemas - Request and response models.
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class CartItemAdd(BaseModel):
    """Add item to cart request schema."""
    product_id: int
    quantity: int = Field(..., ge=1)


class CartItemUpdate(BaseModel):
    """Update cart item quantity request schema."""
    quantity: int = Field(..., ge=0)  # 0 means remove


class CartItemResponse(BaseModel):
    """Cart item response schema."""
    id: int
    product_id: int
    quantity: int
    product: Optional[dict] = None

    class Config:
        from_attributes = True


class CartResponse(BaseModel):
    """Cart response schema."""
    id: int
    user_id: int
    items: List[CartItemResponse] = []
    created_at: datetime

    class Config:
        from_attributes = True


class CartSummary(BaseModel):
    """Cart summary with totals."""
    total_items: int
    total_price: float
    items: List[CartItemResponse]
