"""
Order schemas - Request and response models.
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class OrderItemResponse(BaseModel):
    """Order item response schema."""
    id: int
    product_id: int
    quantity: int
    price: float
    product: Optional[dict] = None

    class Config:
        from_attributes = True


class OrderCreate(BaseModel):
    """Create order from cart request schema."""
    pass  # Order is created from cart, no additional data needed


class OrderResponse(BaseModel):
    """Order response schema."""
    id: int
    user_id: int
    order_number: str
    total_amount: float
    status: str
    items: List[OrderItemResponse] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class OrderStatusUpdate(BaseModel):
    """Update order status request schema."""
    status: str = Field(..., description="New order status")


class OrderDetailResponse(OrderResponse):
    """Detailed order response with user and item details."""
    user: Optional[dict] = None


class OrderListResponse(BaseModel):
    """Order list response with pagination."""
    total: int
    page: int
    page_size: int
    items: List[OrderResponse]
