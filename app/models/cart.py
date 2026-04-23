"""
Cart and CartItem models - Shopping cart functionality.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base


class Cart(Base):
    """
    Cart model for user shopping carts.
    
    Attributes:
        id: Unique identifier (Primary Key)
        user_id: Foreign key to user
        created_at: Cart creation timestamp
        updated_at: Last update timestamp
    """
    __tablename__ = "carts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", backref="carts")
    items = relationship("CartItem", backref="cart", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Cart(id={self.id}, user_id={self.user_id})>"


class CartItem(Base):
    """
    CartItem model for individual items in shopping cart.
    
    Attributes:
        id: Unique identifier (Primary Key)
        cart_id: Foreign key to cart
        product_id: Foreign key to product
        quantity: Number of items
        created_at: Item addition timestamp
    """
    __tablename__ = "cart_items"

    id = Column(Integer, primary_key=True, index=True)
    cart_id = Column(Integer, ForeignKey("carts.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, index=True)
    quantity = Column(Integer, default=1, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    product = relationship("Product", backref="cart_items")

    def __repr__(self):
        return f"<CartItem(id={self.id}, product_id={self.product_id}, quantity={self.quantity})>"
