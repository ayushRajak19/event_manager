"""
Transaction schemas - Request/Response models.
"""
from pydantic import BaseModel
from datetime import datetime


class TransactionRequest(BaseModel):
    """Request model for creating a transaction."""
    user_id: int
    transaction_type: str  # membership_purchase, order_payment, refund
    related_id: int = None
    amount: float
    payment_method: str = "cash"
    description: str = None


class TransactionResponse(BaseModel):
    """Response model for transaction data."""
    id: int
    user_id: int
    transaction_type: str
    related_id: int = None
    amount: float
    payment_method: str
    status: str
    description: str = None
    created_at: datetime

    class Config:
        from_attributes = True


class TransactionListResponse(BaseModel):
    """Response model for transaction list with pagination."""
    total: int
    count: int
    page: int
    limit: int
    transactions: list[TransactionResponse]
