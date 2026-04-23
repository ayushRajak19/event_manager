"""
Cart routes - Shopping cart management endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.db import get_db
from app.core import require_user
from app.schemas.cart import CartItemAdd, CartItemUpdate, CartResponse, CartSummary
from app.services.cart_service import CartService

router = APIRouter(prefix="/carts", tags=["cart"])


@router.get("", response_model=CartResponse, dependencies=[Depends(require_user)])
async def get_cart(
    current_user: dict = Depends(require_user),
    db: Session = Depends(get_db)
):
    """
    Get user's shopping cart.
    
    Returns:
        CartResponse: User's cart with items
    """
    user_id = current_user["user_id"]
    
    cart = CartService.get_cart(db, user_id)
    
    return cart


@router.get("/summary", response_model=CartSummary, dependencies=[Depends(require_user)])
async def get_cart_summary(
    current_user: dict = Depends(require_user),
    db: Session = Depends(get_db)
):
    """
    Get cart summary with totals.
    
    Returns:
        CartSummary: Cart summary with total items and price
    """
    user_id = current_user["user_id"]
    
    summary = CartService.get_cart_summary(db, user_id)
    
    return CartSummary(
        total_items=summary["total_items"],
        total_price=summary["total_price"],
        items=summary["items"]
    )


@router.post("/add", response_model=dict, dependencies=[Depends(require_user)])
async def add_to_cart(
    item: CartItemAdd,
    current_user: dict = Depends(require_user),
    db: Session = Depends(get_db)
):
    """
    Add item to cart.
    
    Args:
        item: Product ID and quantity
        
    Returns:
        dict: Success message with item details
    """
    user_id = current_user["user_id"]
    
    cart_item = CartService.add_to_cart(db, user_id, item)
    
    return {
        "message": "Item added to cart",
        "product_id": cart_item.product_id,
        "quantity": cart_item.quantity
    }


@router.put("/items/{product_id}", response_model=dict, dependencies=[Depends(require_user)])
async def update_cart_item(
    product_id: int,
    update_data: CartItemUpdate,
    current_user: dict = Depends(require_user),
    db: Session = Depends(get_db)
):
    """
    Update cart item quantity.
    
    Args:
        product_id: Product ID
        update_data: New quantity (0 to remove)
        
    Returns:
        dict: Success message
    """
    user_id = current_user["user_id"]
    
    if update_data.quantity == 0:
        CartService.remove_from_cart(db, user_id, product_id)
        return {"message": "Item removed from cart"}
    
    CartService.update_cart_item(db, user_id, product_id, update_data)
    
    return {
        "message": "Cart item updated",
        "product_id": product_id,
        "quantity": update_data.quantity
    }


@router.delete("/items/{product_id}", dependencies=[Depends(require_user)])
async def remove_from_cart(
    product_id: int,
    current_user: dict = Depends(require_user),
    db: Session = Depends(get_db)
):
    """
    Remove item from cart.
    
    Args:
        product_id: Product ID to remove
        
    Returns:
        dict: Success message
    """
    user_id = current_user["user_id"]
    
    CartService.remove_from_cart(db, user_id, product_id)
    
    return {"message": "Item removed from cart"}


@router.delete("", dependencies=[Depends(require_user)])
async def clear_cart(
    current_user: dict = Depends(require_user),
    db: Session = Depends(get_db)
):
    """
    Clear all items from cart.
    
    Returns:
        dict: Success message
    """
    user_id = current_user["user_id"]
    
    CartService.clear_cart(db, user_id)
    
    return {"message": "Cart cleared"}
