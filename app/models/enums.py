"""
Enum definitions for role and status types.
"""
from enum import Enum


class UserRole(str, Enum):
    """User roles in the system."""
    ADMIN = "admin"
    USER = "user"
    VENDOR = "vendor"


class OrderStatus(str, Enum):
    """Order status lifecycle."""
    PENDING = "pending"
    APPROVED = "approved"
    PACKED = "packed"
    DISPATCHED = "dispatched"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class ItemRequestStatus(str, Enum):
    """Status of item requests from users."""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    FULFILLED = "fulfilled"


class ProductStatus(str, Enum):
    """Product availability status."""
    AVAILABLE = "available"
    OUT_OF_STOCK = "out_of_stock"
    DISCONTINUED = "discontinued"


class VendorStatus(str, Enum):
    """Vendor account status."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
