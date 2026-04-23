"""
Order and OrderItem models - Order management.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base
from app.models.enums import OrderStatus


class Order(Base):
    """
    Order model for user purchases.
    
    Attributes:
        id: Unique identifier (Primary Key)
        user_id: Foreign key to user
        order_number: Unique order number for reference
        total_amount: Total order amount
        status: Current order status
        created_at: Order creation timestamp
        updated_at: Last update timestamp
    """
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    order_number = Column(String(50), unique=True, index=True, nullable=False)
    total_amount = Column(Float, default=0.0)
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", backref="orders")
    items = relationship("OrderItem", backref="order", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Order(id={self.id}, order_number={self.order_number}, user_id={self.user_id})>"


class OrderItem(Base):
    """
    OrderItem model for individual items in an order.
    
    Attributes:
        id: Unique identifier (Primary Key)
        order_id: Foreign key to order
        product_id: Foreign key to product
        quantity: Number of items ordered
        price: Price per unit at time of order
        created_at: Item addition timestamp
    """
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, index=True)
    quantity = Column(Integer, default=1, nullable=False)
    price = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    product = relationship("Product", backref="order_items")

    def __repr__(self):
        return f"<OrderItem(id={self.id}, product_id={self.product_id}, quantity={self.quantity})>"
