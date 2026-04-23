"""
Product model - Event items/products.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base
from app.models.enums import ProductStatus


class Product(Base):
    """
    Product model for event items available in the system.
    
    Attributes:
        id: Unique identifier (Primary Key)
        name: Product name
        description: Detailed product description
        category: Product category (e.g., Audio, Lighting, Decor)
        quantity: Available quantity in stock
        price: Price per unit
        status: Availability status
        vendor_id: Foreign key to vendor
        created_at: Product creation timestamp
        updated_at: Last update timestamp
    """
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(String(1000), nullable=True)
    category = Column(String(100), nullable=True)
    quantity = Column(Integer, default=0)
    price = Column(Float, nullable=False)
    status = Column(Enum(ProductStatus), default=ProductStatus.AVAILABLE)
    vendor_id = Column(Integer, ForeignKey("vendors.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    vendor = relationship("Vendor", backref="products")

    def __repr__(self):
        return f"<Product(id={self.id}, name={self.name}, vendor_id={self.vendor_id})>"
