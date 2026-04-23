"""
Vendor model - Event item suppliers.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Enum
from app.db.base import Base
from app.models.enums import VendorStatus


class Vendor(Base):
    """
    Vendor model for suppliers who provide event items.
    
    Attributes:
        id: Unique identifier (Primary Key)
        name: Vendor name
        email: Vendor email (unique)
        password_hash: Hashed password for secure storage
        company_name: Company name
        phone: Contact phone number
        status: Current status (active, inactive, suspended)
        created_at: Account creation timestamp
    """
    __tablename__ = "vendors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    company_name = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=True)
    status = Column(Enum(VendorStatus), default=VendorStatus.ACTIVE)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Vendor(id={self.id}, email={self.email}, company_name={self.company_name})>"
