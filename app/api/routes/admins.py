"""
Admin routes - Admin dashboard and management endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.db import get_db
from app.core import require_admin
from app.models import User, Vendor, Order, ItemRequest
from app.schemas.auth import UserResponse, VendorResponse
from app.services.order_service import OrderService
from app.services.item_request_service import ItemRequestService

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/dashboard", dependencies=[Depends(require_admin)])
async def admin_dashboard(
    current_user: dict = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """
    Admin dashboard - Overview statistics.
    
    Returns summary statistics for the platform.
    """
    total_users = db.query(User).count()
    total_vendors = db.query(Vendor).count()
    total_orders = db.query(Order).count()
    pending_requests = db.query(ItemRequest).filter(
        ItemRequest.status == "pending"
    ).count()
    
    return {
        "total_users": total_users,
        "total_vendors": total_vendors,
        "total_orders": total_orders,
        "pending_item_requests": pending_requests,
        "message": "Admin dashboard"
    }


@router.get("/users", response_model=dict, dependencies=[Depends(require_admin)])
async def get_all_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    current_user: dict = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """
    Get all users - Admin view.
    
    Args:
        skip: Number of users to skip
        limit: Maximum users to return
        
    Returns:
        dict: Paginated user list
    """
    query = db.query(User)
    total = query.count()
    users = query.offset(skip).limit(limit).all()
    
    return {
        "total": total,
        "page": skip // limit + 1 if limit > 0 else 1,
        "page_size": limit,
        "items": users
    }


@router.get("/users/{user_id}", response_model=UserResponse, dependencies=[Depends(require_admin)])
async def get_user_details(
    user_id: int,
    current_user: dict = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """
    Get specific user details.
    
    Args:
        user_id: User ID to retrieve
        
    Returns:
        UserResponse: User details
    """
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user


@router.put("/users/{user_id}/deactivate", dependencies=[Depends(require_admin)])
async def deactivate_user(
    user_id: int,
    current_user: dict = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """
    Deactivate a user account.
    
    Args:
        user_id: User ID to deactivate
        
    Returns:
        dict: Success message
    """
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    user.is_active = 0
    db.commit()
    
    return {"message": "User deactivated successfully"}


@router.get("/vendors", response_model=dict, dependencies=[Depends(require_admin)])
async def get_all_vendors(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    current_user: dict = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """
    Get all vendors - Admin view.
    
    Args:
        skip: Number of vendors to skip
        limit: Maximum vendors to return
        
    Returns:
        dict: Paginated vendor list
    """
    query = db.query(Vendor)
    total = query.count()
    vendors = query.offset(skip).limit(limit).all()
    
    return {
        "total": total,
        "page": skip // limit + 1 if limit > 0 else 1,
        "page_size": limit,
        "items": vendors
    }


@router.get("/vendors/{vendor_id}", response_model=VendorResponse, dependencies=[Depends(require_admin)])
async def get_vendor_details(
    vendor_id: int,
    current_user: dict = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """
    Get specific vendor details.
    
    Args:
        vendor_id: Vendor ID to retrieve
        
    Returns:
        VendorResponse: Vendor details
    """
    vendor = db.query(Vendor).filter(Vendor.id == vendor_id).first()
    
    if not vendor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vendor not found"
        )
    
    return vendor


@router.get("/orders", response_model=dict, dependencies=[Depends(require_admin)])
async def get_all_orders(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    status: str = Query(None),
    current_user: dict = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """
    Get all orders - Admin view.
    
    Args:
        skip: Number of orders to skip
        limit: Maximum orders to return
        status: Filter by order status
        
    Returns:
        dict: Paginated order list
    """
    total, orders = OrderService.get_all_orders(db, skip, limit, status)
    
    return {
        "total": total,
        "page": skip // limit + 1 if limit > 0 else 1,
        "page_size": limit,
        "items": orders
    }


@router.get("/item-requests", response_model=dict, dependencies=[Depends(require_admin)])
async def get_all_item_requests(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    current_user: dict = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """
    Get all item requests - Admin view.
    
    Args:
        skip: Number of requests to skip
        limit: Maximum requests to return
        
    Returns:
        dict: Paginated item request list
    """
    query = db.query(ItemRequest)
    total = query.count()
    requests = query.order_by(ItemRequest.created_at.desc()).offset(skip).limit(limit).all()
    
    return {
        "total": total,
        "page": skip // limit + 1 if limit > 0 else 1,
        "page_size": limit,
        "items": requests
    }
