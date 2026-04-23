"""
Cart service - Shopping cart business logic.
"""
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models import Cart, CartItem, Product
from app.schemas.cart import CartItemAdd, CartItemUpdate


class CartService:
    """Service for cart operations."""

    @staticmethod
    def get_or_create_cart(db: Session, user_id: int) -> Cart:
        """
        Get user's cart or create if doesn't exist.
        
        Args:
            db: Database session
            user_id: User ID
            
        Returns:
            Cart: User's cart
        """
        cart = db.query(Cart).filter(Cart.user_id == user_id).first()
        
        if not cart:
            cart = Cart(user_id=user_id)
            db.add(cart)
            db.commit()
            db.refresh(cart)
        
        return cart

    @staticmethod
    def add_to_cart(
        db: Session,
        user_id: int,
        cart_item_data: CartItemAdd
    ) -> CartItem:
        """
        Add item to user's cart.
        
        Args:
            db: Database session
            user_id: User ID
            cart_item_data: Item to add
            
        Returns:
            CartItem: Added or updated cart item
            
        Raises:
            HTTPException: If product not found or out of stock
        """
        # Get or create cart
        cart = CartService.get_or_create_cart(db, user_id)
        
        # Check if product exists and is available
        product = db.query(Product).filter(Product.id == cart_item_data.product_id).first()
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )
        
        if product.quantity < cart_item_data.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Insufficient stock. Available: {product.quantity}"
            )
        
        # Check if item already in cart
        cart_item = db.query(CartItem).filter(
            CartItem.cart_id == cart.id,
            CartItem.product_id == cart_item_data.product_id
        ).first()
        
        if cart_item:
            cart_item.quantity += cart_item_data.quantity
        else:
            cart_item = CartItem(
                cart_id=cart.id,
                product_id=cart_item_data.product_id,
                quantity=cart_item_data.quantity
            )
            db.add(cart_item)
        
        db.commit()
        db.refresh(cart_item)
        
        return cart_item

    @staticmethod
    def remove_from_cart(
        db: Session,
        user_id: int,
        product_id: int
    ) -> bool:
        """
        Remove item from cart.
        
        Args:
            db: Database session
            user_id: User ID
            product_id: Product ID to remove
            
        Returns:
            bool: True if removed
            
        Raises:
            HTTPException: If item not in cart
        """
        cart = CartService.get_or_create_cart(db, user_id)
        
        cart_item = db.query(CartItem).filter(
            CartItem.cart_id == cart.id,
            CartItem.product_id == product_id
        ).first()
        
        if not cart_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Item not found in cart"
            )
        
        db.delete(cart_item)
        db.commit()
        
        return True

    @staticmethod
    def update_cart_item(
        db: Session,
        user_id: int,
        product_id: int,
        cart_item_data: CartItemUpdate
    ) -> CartItem:
        """
        Update cart item quantity.
        
        Args:
            db: Database session
            user_id: User ID
            product_id: Product ID
            cart_item_data: Updated quantity
            
        Returns:
            CartItem: Updated cart item
            
        Raises:
            HTTPException: If item not in cart or invalid quantity
        """
        cart = CartService.get_or_create_cart(db, user_id)
        
        cart_item = db.query(CartItem).filter(
            CartItem.cart_id == cart.id,
            CartItem.product_id == product_id
        ).first()
        
        if not cart_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Item not found in cart"
            )
        
        if cart_item_data.quantity == 0:
            db.delete(cart_item)
            db.commit()
            return None
        
        # Check stock
        product = db.query(Product).filter(Product.id == product_id).first()
        if product.quantity < cart_item_data.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Insufficient stock. Available: {product.quantity}"
            )
        
        cart_item.quantity = cart_item_data.quantity
        db.commit()
        db.refresh(cart_item)
        
        return cart_item

    @staticmethod
    def get_cart(db: Session, user_id: int) -> Cart:
        """
        Get user's cart with items.
        
        Args:
            db: Database session
            user_id: User ID
            
        Returns:
            Cart: User's cart
        """
        return CartService.get_or_create_cart(db, user_id)

    @staticmethod
    def clear_cart(db: Session, user_id: int) -> bool:
        """
        Clear all items from user's cart.
        
        Args:
            db: Database session
            user_id: User ID
            
        Returns:
            bool: True if cleared
        """
        cart = CartService.get_or_create_cart(db, user_id)
        
        db.query(CartItem).filter(CartItem.cart_id == cart.id).delete()
        db.commit()
        
        return True

    @staticmethod
    def get_cart_summary(db: Session, user_id: int) -> dict:
        """
        Get cart summary with totals.
        
        Args:
            db: Database session
            user_id: User ID
            
        Returns:
            dict: Cart summary with total items and price
        """
        cart = CartService.get_or_create_cart(db, user_id)
        
        items = db.query(CartItem).filter(CartItem.cart_id == cart.id).all()
        
        total_items = sum(item.quantity for item in items)
        total_price = sum(item.product.price * item.quantity for item in items if item.product)
        
        return {
            "total_items": total_items,
            "total_price": total_price,
            "items": items
        }
