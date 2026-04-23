"""
Admin model - Administrative users.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from app.db.base import Base


class Admin(Base):
    """
    Admin model for system administrators.
    
    Attributes:
        id: Unique identifier (Primary Key)
        name: Admin name
        email: Admin email (unique)
        password_hash: Hashed password for secure storage
        created_at: Account creation timestamp
    """
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Admin(id={self.id}, email={self.email}, name={self.name})>"
