"""
Checkout routes - Order creation from cart.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db import get_db
from app.core import require_user
from app.schemas.order import OrderResponse
from app.services.order_service import OrderService

router = APIRouter(prefix="/checkout", tags=["checkout"])


@router.post("/place-order", response_model=OrderResponse, dependencies=[Depends(require_user)])
async def place_order(
    current_user: dict = Depends(require_user),
    db: Session = Depends(get_db)
):
    """
    Create order from cart (checkout).
    
    Converts cart items to order, calculates total,
    reduces inventory, and returns order details.
    
    Returns:
        OrderResponse: Created order details
        
    Raises:
        HTTPException: If cart is empty
    """
    user_id = current_user["user_id"]
    
    order = OrderService.create_order_from_cart(db, user_id)
    
    return order


@router.get("/success/{order_id}", response_model=dict, dependencies=[Depends(require_user)])
async def order_success(
    order_id: int,
    current_user: dict = Depends(require_user),
    db: Session = Depends(get_db)
):
    """
    Order success page - Retrieve order confirmation.
    
    Args:
        order_id: Order ID
        
    Returns:
        dict: Order confirmation details
    """
    user_id = current_user["user_id"]
    
    order = OrderService.get_order(db, order_id)
    
    # Verify order belongs to current user
    if order.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this order"
        )
    
    return {
        "message": "Order placed successfully",
        "order_number": order.order_number,
        "order_id": order.id,
        "total_amount": order.total_amount,
        "status": order.status,
        "items_count": len(order.items),
        "created_at": order.created_at
    }
