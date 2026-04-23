"""
Order service - Order management business logic.
"""
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime
from app.models import Order, OrderItem, CartItem, Product
from app.schemas.order import OrderCreate, OrderStatusUpdate
from app.services.cart_service import CartService
import uuid


class OrderService:
    """Service for order operations."""

    @staticmethod
    def create_order_from_cart(db: Session, user_id: int) -> Order:
        """
        Create an order from user's cart.
        
        Args:
            db: Database session
            user_id: User ID
            
        Returns:
            Order: Created order
            
        Raises:
            HTTPException: If cart is empty
        """
        # Get cart items
        cart = CartService.get_or_create_cart(db, user_id)
        cart_items = db.query(CartItem).filter(CartItem.cart_id == cart.id).all()
        
        if not cart_items:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cart is empty"
            )
        
        # Calculate total amount
        total_amount = sum(item.product.price * item.quantity for item in cart_items)
        
        # Create order
        order_number = f"ORD-{user_id}-{int(datetime.utcnow().timestamp())}"
        new_order = Order(
            user_id=user_id,
            order_number=order_number,
            total_amount=total_amount,
            status="pending"
        )
        
        db.add(new_order)
        db.flush()  # Get order ID without committing
        
        # Create order items from cart items
        for cart_item in cart_items:
            order_item = OrderItem(
                order_id=new_order.id,
                product_id=cart_item.product_id,
                quantity=cart_item.quantity,
                price=cart_item.product.price
            )
            db.add(order_item)
            
            # Update product quantity
            product = cart_item.product
            product.quantity -= cart_item.quantity
        
        # Clear cart
        CartService.clear_cart(db, user_id)
        
        db.commit()
        db.refresh(new_order)
        
        return new_order

    @staticmethod
    def get_order(db: Session, order_id: int) -> Order:
        """
        Get order by ID.
        
        Args:
            db: Database session
            order_id: Order ID
            
        Returns:
            Order: Order object
            
        Raises:
            HTTPException: If order not found
        """
        order = db.query(Order).filter(Order.id == order_id).first()
        
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found"
            )
        
        return order

    @staticmethod
    def get_order_by_number(db: Session, order_number: str) -> Order:
        """
        Get order by order number.
        
        Args:
            db: Database session
            order_number: Order number
            
        Returns:
            Order: Order object
            
        Raises:
            HTTPException: If order not found
        """
        order = db.query(Order).filter(Order.order_number == order_number).first()
        
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found"
            )
        
        return order

    @staticmethod
    def get_user_orders(
        db: Session,
        user_id: int,
        skip: int = 0,
        limit: int = 10,
        status: str = None
    ) -> tuple:
        """
        Get user's orders with optional filtering.
        
        Args:
            db: Database session
            user_id: User ID
            skip: Number of items to skip
            limit: Maximum items to return
            status: Filter by status
            
        Returns:
            tuple: (total_count, orders_list)
        """
        query = db.query(Order).filter(Order.user_id == user_id)
        
        if status:
            query = query.filter(Order.status == status)
        
        total = query.count()
        orders = query.order_by(Order.created_at.desc()).offset(skip).limit(limit).all()
        
        return total, orders

    @staticmethod
    def get_all_orders(
        db: Session,
        skip: int = 0,
        limit: int = 10,
        status: str = None
    ) -> tuple:
        """
        Get all orders (admin view).
        
        Args:
            db: Database session
            skip: Number of items to skip
            limit: Maximum items to return
            status: Filter by status
            
        Returns:
            tuple: (total_count, orders_list)
        """
        query = db.query(Order)
        
        if status:
            query = query.filter(Order.status == status)
        
        total = query.count()
        orders = query.order_by(Order.created_at.desc()).offset(skip).limit(limit).all()
        
        return total, orders

    @staticmethod
    def update_order_status(
        db: Session,
        order_id: int,
        status_update: OrderStatusUpdate
    ) -> Order:
        """
        Update order status.
        
        Args:
            db: Database session
            order_id: Order ID
            status_update: New status
            
        Returns:
            Order: Updated order
            
        Raises:
            HTTPException: If order not found
        """
        order = OrderService.get_order(db, order_id)
        order.status = status_update.status
        
        db.commit()
        db.refresh(order)
        
        return order

    @staticmethod
    def cancel_order(db: Session, order_id: int) -> Order:
        """
        Cancel an order and restore product quantities.
        
        Args:
            db: Database session
            order_id: Order ID
            
        Returns:
            Order: Updated order
            
        Raises:
            HTTPException: If order not found or already dispatched
        """
        order = OrderService.get_order(db, order_id)
        
        # Cannot cancel dispatched or delivered orders
        if order.status in ["dispatched", "delivered"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot cancel dispatched or delivered orders"
            )
        
        # Restore product quantities
        for order_item in order.items:
            product = order_item.product
            product.quantity += order_item.quantity
        
        order.status = "cancelled"
        
        db.commit()
        db.refresh(order)
        
        return order
