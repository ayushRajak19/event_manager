"""
Order routes - Order tracking and management.
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.db import get_db
from app.core import require_user, require_admin, require_vendor, get_current_user
from app.schemas.order import OrderResponse, OrderListResponse, OrderStatusUpdate
from app.services.order_service import OrderService

router = APIRouter(prefix="/orders", tags=["orders"])


@router.get("/my-orders", response_model=dict, dependencies=[Depends(require_user)])
async def get_user_orders(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    status: str = Query(None),
    current_user: dict = Depends(require_user),
    db: Session = Depends(get_db)
):
    """
    Get current user's orders.
    
    Args:
        skip: Number of orders to skip
        limit: Maximum orders to return
        status: Filter by order status
        
    Returns:
        dict: Paginated order list
    """
    user_id = current_user["user_id"]
    
    total, orders = OrderService.get_user_orders(db, user_id, skip, limit, status)
    
    return {
        "total": total,
        "page": skip // limit + 1 if limit > 0 else 1,
        "page_size": limit,
        "items": orders
    }


@router.get("/{order_id}", response_model=OrderResponse, dependencies=[Depends(require_user)])
async def get_order(
    order_id: int,
    current_user: dict = Depends(require_user),
    db: Session = Depends(get_db)
):
    """
    Get order details.
    
    Args:
        order_id: Order ID
        
    Returns:
        OrderResponse: Order details
    """
    user_id = current_user["user_id"]
    
    order = OrderService.get_order(db, order_id)
    
    # Verify authorization
    if order.user_id != user_id and current_user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this order"
        )
    
    return order


@router.get("/by-number/{order_number}", response_model=OrderResponse, dependencies=[Depends(require_user)])
async def get_order_by_number(
    order_number: str,
    current_user: dict = Depends(require_user),
    db: Session = Depends(get_db)
):
    """
    Get order by order number.
    
    Args:
        order_number: Order number
        
    Returns:
        OrderResponse: Order details
    """
    order = OrderService.get_order_by_number(db, order_number)
    
    # Verify authorization
    if order.user_id != current_user["user_id"] and current_user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this order"
        )
    
    return order


@router.put("/{order_id}/status", response_model=OrderResponse, dependencies=[Depends(require_admin)])
async def update_order_status(
    order_id: int,
    status_update: OrderStatusUpdate,
    current_user: dict = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """
    Update order status (admin/vendor only).
    
    Args:
        order_id: Order ID
        status_update: New status
        
    Returns:
        OrderResponse: Updated order
    """
    # Only admin or vendor can update order status
    if current_user["role"] not in ["admin", "vendor"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update order status"
        )
    
    return OrderService.update_order_status(db, order_id, status_update)


@router.post("/{order_id}/cancel", response_model=OrderResponse, dependencies=[Depends(require_user)])
async def cancel_order(
    order_id: int,
    current_user: dict = Depends(require_user),
    db: Session = Depends(get_db)
):
    """
    Cancel an order.
    
    Args:
        order_id: Order ID
        
    Returns:
        OrderResponse: Updated order with cancelled status
    """
    user_id = current_user["user_id"]
    
    order = OrderService.get_order(db, order_id)
    
    # Verify ownership
    if order.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to cancel this order"
        )
    
    return OrderService.cancel_order(db, order_id)
