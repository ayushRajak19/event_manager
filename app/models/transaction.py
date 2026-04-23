"""
Transaction model - Track all membership and order transactions.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Float, Text
from app.db.base import Base


class Transaction(Base):
    """
    Transaction model for tracking all payments and transactions.
    
    Attributes:
        id: Unique identifier (Primary Key)
        user_id: User making the transaction
        transaction_type: membership_purchase, order_payment, refund
        related_id: ID of related membership or order
        amount: Transaction amount
        payment_method: Cash, Card, UPI, etc.
        status: Pending, Completed, Failed, Refunded
        description: Transaction details
        created_at: Transaction timestamp
    """
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    transaction_type = Column(String(50), nullable=False)  # membership_purchase, order_payment, refund
    related_id = Column(Integer, nullable=True)  # ID of membership or order
    amount = Column(Float, nullable=False)
    payment_method = Column(String(50), default="cash")  # cash, card, upi, online
    status = Column(String(50), default="pending")  # pending, completed, failed, refunded
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    def __repr__(self):
        return f"<Transaction(id={self.id}, user_id={self.user_id}, type={self.transaction_type}, status={self.status})>"
