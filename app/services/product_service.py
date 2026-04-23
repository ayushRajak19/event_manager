"""
Product service - Product management business logic.
"""
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models import Product
from app.schemas.product import ProductCreate, ProductUpdate


class ProductService:
    """Service for product operations."""

    @staticmethod
    def create_product(db: Session, product_data: ProductCreate, vendor_id: int) -> Product:
        """
        Create a new product.
        
        Args:
            db: Database session
            product_data: Product creation data
            vendor_id: ID of vendor creating the product
            
        Returns:
            Product: Created product
        """
        new_product = Product(
            name=product_data.name,
            description=product_data.description,
            category=product_data.category,
            quantity=product_data.quantity,
            price=product_data.price,
            status=product_data.status,
            vendor_id=vendor_id
        )
        
        db.add(new_product)
        db.commit()
        db.refresh(new_product)
        
        return new_product

    @staticmethod
    def get_product(db: Session, product_id: int) -> Product:
        """
        Get product by ID.
        
        Args:
            db: Database session
            product_id: Product ID
            
        Returns:
            Product: Product object
            
        Raises:
            HTTPException: If product not found
        """
        product = db.query(Product).filter(Product.id == product_id).first()
        
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )
        
        return product

    @staticmethod
    def get_all_products(
        db: Session,
        skip: int = 0,
        limit: int = 10,
        category: str = None,
        status: str = None
    ) -> tuple:
        """
        Get all products with optional filtering.
        
        Args:
            db: Database session
            skip: Number of items to skip
            limit: Maximum items to return
            category: Filter by category
            status: Filter by status
            
        Returns:
            tuple: (total_count, products_list)
        """
        query = db.query(Product)
        
        if category:
            query = query.filter(Product.category == category)
        
        if status:
            query = query.filter(Product.status == status)
        
        total = query.count()
        products = query.offset(skip).limit(limit).all()
        
        return total, products

    @staticmethod
    def get_vendor_products(
        db: Session,
        vendor_id: int,
        skip: int = 0,
        limit: int = 10
    ) -> tuple:
        """
        Get products for a specific vendor.
        
        Args:
            db: Database session
            vendor_id: Vendor ID
            skip: Number of items to skip
            limit: Maximum items to return
            
        Returns:
            tuple: (total_count, products_list)
        """
        query = db.query(Product).filter(Product.vendor_id == vendor_id)
        total = query.count()
        products = query.offset(skip).limit(limit).all()
        
        return total, products

    @staticmethod
    def update_product(
        db: Session,
        product_id: int,
        product_data: ProductUpdate,
        vendor_id: int
    ) -> Product:
        """
        Update a product.
        
        Args:
            db: Database session
            product_id: Product ID
            product_data: Updated product data
            vendor_id: Vendor ID (for authorization)
            
        Returns:
            Product: Updated product
            
        Raises:
            HTTPException: If product not found or unauthorized
        """
        product = ProductService.get_product(db, product_id)
        
        # Check authorization
        if product.vendor_id != vendor_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to update this product"
            )
        
        # Update fields
        if product_data.name is not None:
            product.name = product_data.name
        if product_data.description is not None:
            product.description = product_data.description
        if product_data.category is not None:
            product.category = product_data.category
        if product_data.quantity is not None:
            product.quantity = product_data.quantity
        if product_data.price is not None:
            product.price = product_data.price
        if product_data.status is not None:
            product.status = product_data.status
        
        db.commit()
        db.refresh(product)
        
        return product

    @staticmethod
    def delete_product(
        db: Session,
        product_id: int,
        vendor_id: int
    ) -> bool:
        """
        Delete a product.
        
        Args:
            db: Database session
            product_id: Product ID
            vendor_id: Vendor ID (for authorization)
            
        Returns:
            bool: True if deleted
            
        Raises:
            HTTPException: If product not found or unauthorized
        """
        product = ProductService.get_product(db, product_id)
        
        # Check authorization
        if product.vendor_id != vendor_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to delete this product"
            )
        
        db.delete(product)
        db.commit()
        
        return True

    @staticmethod
    def update_quantity(
        db: Session,
        product_id: int,
        quantity_change: int
    ) -> Product:
        """
        Update product quantity (for inventory management).
        
        Args:
            db: Database session
            product_id: Product ID
            quantity_change: Change in quantity (positive or negative)
            
        Returns:
            Product: Updated product
        """
        product = ProductService.get_product(db, product_id)
        product.quantity = max(0, product.quantity + quantity_change)
        
        db.commit()
        db.refresh(product)
        
        return product
