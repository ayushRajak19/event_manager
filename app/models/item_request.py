"""
ItemRequest model - User requests for unavailable items.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base
from app.models.enums import ItemRequestStatus


class ItemRequest(Base):
    """
    ItemRequest model for user requests of items not in catalog.
    
    Attributes:
        id: Unique identifier (Primary Key)
        user_id: Foreign key to requesting user
        item_name: Name of requested item
        description: Detailed description of requested item
        category: Item category
        status: Request status (pending, approved, fulfilled, rejected)
        vendor_id: Optional vendor assigned to fulfill request
        created_at: Request creation timestamp
        updated_at: Last update timestamp
    """
    __tablename__ = "item_requests"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    item_name = Column(String(255), nullable=False)
    description = Column(String(1000), nullable=True)
    category = Column(String(100), nullable=True)
    status = Column(Enum(ItemRequestStatus), default=ItemRequestStatus.PENDING)
    vendor_id = Column(Integer, ForeignKey("vendors.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", backref="item_requests")
    vendor = relationship("Vendor", backref="item_requests")

    def __repr__(self):
        return f"<ItemRequest(id={self.id}, item_name={self.item_name}, user_id={self.user_id})>"
