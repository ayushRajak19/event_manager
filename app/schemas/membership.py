"""
Membership schemas - Request/Response models.
"""
from pydantic import BaseModel
from datetime import datetime


class MembershipRequest(BaseModel):
    """Request model for creating/updating membership."""
    user_id: int
    membership_type: str  # 6_months, 1_year, 2_years
    amount_paid: float


class MembershipResponse(BaseModel):
    """Response model for membership data."""
    id: int
    user_id: int
    membership_number: str
    membership_type: str
    start_date: datetime
    expiry_date: datetime
    amount_paid: float
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class MembershipExtendRequest(BaseModel):
    """Request model for extending membership."""
    membership_id: int
    new_type: str  # 6_months, 1_year, 2_years
    amount_paid: float
