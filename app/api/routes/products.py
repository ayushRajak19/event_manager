"""
Product routes - Product catalog endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.db import get_db
from app.core import get_current_user
from app.models import Product
from app.schemas.product import ProductResponse, ProductDetailResponse

router = APIRouter(prefix="/products", tags=["products"])


@router.get("", response_model=dict)
async def get_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    category: str = Query(None),
    status: str = Query(None),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all available products with filtering.
    
    Args:
        skip: Number of products to skip
        limit: Maximum products to return
        category: Filter by category
        status: Filter by status
        
    Returns:
        dict: Paginated product list
    """
    query = db.query(Product)
    
    if category:
        query = query.filter(Product.category == category)
    
    if status:
        query = query.filter(Product.status == status)
    
    total = query.count()
    products = query.offset(skip).limit(limit).all()
    
    return {
        "total": total,
        "page": skip // limit + 1 if limit > 0 else 1,
        "page_size": limit,
        "items": products
    }


@router.get("/{product_id}", response_model=ProductDetailResponse)
async def get_product_detail(
    product_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get product details.
    
    Args:
        product_id: Product ID
        
    Returns:
        ProductDetailResponse: Product details with vendor info
    """
    product = db.query(Product).filter(Product.id == product_id).first()
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    return product


@router.get("/categories", response_model=dict)
async def get_categories(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all product categories.
    
    Returns:
        dict: List of categories
    """
    categories = db.query(Product.category).distinct().filter(
        Product.category.isnot(None)
    ).all()
    
    category_list = [cat[0] for cat in categories if cat[0]]
    
    return {
        "total": len(category_list),
        "items": category_list
    }


@router.get("/search/", response_model=dict)
async def search_products(
    query: str = Query(..., min_length=1),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Search products by name or description.
    
    Args:
        query: Search query
        skip: Number of results to skip
        limit: Maximum results to return
        
    Returns:
        dict: Search results
    """
    search_query = f"%{query}%"
    
    db_query = db.query(Product).filter(
        (Product.name.ilike(search_query)) |
        (Product.description.ilike(search_query))
    )
    
    total = db_query.count()
    products = db_query.offset(skip).limit(limit).all()
    
    return {
        "total": total,
        "page": skip // limit + 1 if limit > 0 else 1,
        "page_size": limit,
        "query": query,
        "items": products
    }
