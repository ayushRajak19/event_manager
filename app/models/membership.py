"""
Membership model - User membership/subscription system.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Float
from app.db.base import Base


class Membership(Base):
    """
    Membership model for user subscriptions.
    
    Attributes:
        id: Unique identifier (Primary Key)
        user_id: Foreign key to User
        membership_number: Unique membership identifier
        membership_type: Duration type (6_months, 1_year, 2_years)
        start_date: Membership start date
        expiry_date: Membership expiration date
        amount_paid: Amount paid for membership
        status: Active/Inactive/Expired
        created_at: Creation timestamp
        updated_at: Last update timestamp
    """
    __tablename__ = "memberships"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    membership_number = Column(String(255), unique=True, nullable=False, index=True)
    membership_type = Column(String(50), nullable=False)  # 6_months, 1_year, 2_years
    start_date = Column(DateTime, default=datetime.utcnow)
    expiry_date = Column(DateTime, nullable=False)
    amount_paid = Column(Float, nullable=False)
    status = Column(String(50), default="active")  # active, inactive, expired, cancelled
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Membership(id={self.id}, user_id={self.user_id}, number={self.membership_number})>"
