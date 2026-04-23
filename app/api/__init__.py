"""
API package - Routes initialization.
"""
from fastapi import APIRouter
from app.api.routes import (
    auth, admins, vendors, users, products, carts, checkout, 
    orders, item_requests, memberships, transactions, admin_management
)

# Create main API router with /api prefix
api_router = APIRouter(prefix="/api")

# Include all route modules
api_router.include_router(auth.router)
api_router.include_router(admins.router)
api_router.include_router(vendors.router)
api_router.include_router(users.router)
api_router.include_router(products.router)
api_router.include_router(carts.router)
api_router.include_router(checkout.router)
api_router.include_router(orders.router)
api_router.include_router(item_requests.router)
api_router.include_router(memberships.router)
api_router.include_router(transactions.router)
api_router.include_router(admin_management.router)

__all__ = ["api_router"]
