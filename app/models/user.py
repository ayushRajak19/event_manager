"""
User model - Regular platform users.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from app.db.base import Base


class User(Base):
    """
    User model for regular platform users who place orders.
    
    Attributes:
        id: Unique identifier (Primary Key)
        name: User full name
        email: User email (unique)
        password_hash: Hashed password for secure storage
        phone: Contact phone number
        created_at: Account creation timestamp
        is_active: Whether user account is active
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Integer, default=1)  # 1 = True, 0 = False

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, name={self.name})>"
