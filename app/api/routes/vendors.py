"""
Vendor routes - Vendor dashboard and management endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.db import get_db
from app.core import require_vendor
from app.models import Vendor
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse
from app.services.product_service import ProductService
from app.services.item_request_service import ItemRequestService

router = APIRouter(prefix="/vendors", tags=["vendor"])


@router.get("/dashboard", dependencies=[Depends(require_vendor)])
async def vendor_dashboard(
    current_user: dict = Depends(require_vendor),
    db: Session = Depends(get_db)
):
    """
    Vendor dashboard - Overview of vendor's operations.
    
    Returns statistics about vendor's products and requests.
    """
    vendor_id = current_user["user_id"]
    
    vendor = db.query(Vendor).filter(Vendor.id == vendor_id).first()
    
    if not vendor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vendor not found"
        )
    
    total_products, _ = ProductService.get_vendor_products(db, vendor_id, limit=0)
    _, pending_requests = ItemRequestService.get_pending_requests(db, limit=0)
    
    return {
        "vendor_id": vendor_id,
        "vendor_name": vendor.company_name,
        "total_products": total_products,
        "pending_requests": len(pending_requests) if pending_requests else 0,
        "status": vendor.status
    }


@router.post("/products", response_model=ProductResponse, dependencies=[Depends(require_vendor)])
async def create_product(
    product_data: ProductCreate,
    current_user: dict = Depends(require_vendor),
    db: Session = Depends(get_db)
):
    """
    Create a new product.
    
    Args:
        product_data: Product details
        
    Returns:
        ProductResponse: Created product
    """
    vendor_id = current_user["user_id"]
    
    return ProductService.create_product(db, product_data, vendor_id)


@router.get("/products", response_model=dict, dependencies=[Depends(require_vendor)])
async def get_vendor_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    current_user: dict = Depends(require_vendor),
    db: Session = Depends(get_db)
):
    """
    Get vendor's products.
    
    Args:
        skip: Number of products to skip
        limit: Maximum products to return
        
    Returns:
        dict: Paginated product list
    """
    vendor_id = current_user["user_id"]
    
    total, products = ProductService.get_vendor_products(db, vendor_id, skip, limit)
    
    return {
        "total": total,
        "page": skip // limit + 1 if limit > 0 else 1,
        "page_size": limit,
        "items": products
    }


@router.get("/products/{product_id}", response_model=ProductResponse, dependencies=[Depends(require_vendor)])
async def get_product(
    product_id: int,
    current_user: dict = Depends(require_vendor),
    db: Session = Depends(get_db)
):
    """
    Get specific product details.
    
    Args:
        product_id: Product ID
        
    Returns:
        ProductResponse: Product details
    """
    product = ProductService.get_product(db, product_id)
    
    # Check authorization
    if product.vendor_id != current_user["user_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this product"
        )
    
    return product


@router.put("/products/{product_id}", response_model=ProductResponse, dependencies=[Depends(require_vendor)])
async def update_product(
    product_id: int,
    product_data: ProductUpdate,
    current_user: dict = Depends(require_vendor),
    db: Session = Depends(get_db)
):
    """
    Update a product.
    
    Args:
        product_id: Product ID
        product_data: Updated product details
        
    Returns:
        ProductResponse: Updated product
    """
    vendor_id = current_user["user_id"]
    
    return ProductService.update_product(db, product_id, product_data, vendor_id)


@router.delete("/products/{product_id}", dependencies=[Depends(require_vendor)])
async def delete_product(
    product_id: int,
    current_user: dict = Depends(require_vendor),
    db: Session = Depends(get_db)
):
    """
    Delete a product.
    
    Args:
        product_id: Product ID
        
    Returns:
        dict: Success message
    """
    vendor_id = current_user["user_id"]
    
    ProductService.delete_product(db, product_id, vendor_id)
    
    return {"message": "Product deleted successfully"}


@router.get("/item-requests", response_model=dict, dependencies=[Depends(require_vendor)])
async def get_vendor_item_requests(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    status: str = Query(None),
    current_user: dict = Depends(require_vendor),
    db: Session = Depends(get_db)
):
    """
    Get item requests assigned to vendor.
    
    Args:
        skip: Number of requests to skip
        limit: Maximum requests to return
        status: Filter by status
        
    Returns:
        dict: Paginated item request list
    """
    vendor_id = current_user["user_id"]
    
    total, requests = ItemRequestService.get_vendor_requests(db, vendor_id, skip, limit, status)
    
    return {
        "total": total,
        "page": skip // limit + 1 if limit > 0 else 1,
        "page_size": limit,
        "items": requests
    }
