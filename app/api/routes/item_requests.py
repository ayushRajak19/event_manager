"""
Item request routes - User item request management.
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.db import get_db
from app.core import require_user, require_admin, require_vendor, get_current_user
from app.schemas.item_request import (
    ItemRequestCreate, ItemRequestResponse, ItemRequestStatusUpdate
)
from app.services.item_request_service import ItemRequestService

router = APIRouter(prefix="/item-requests", tags=["item-requests"])


@router.post("", response_model=ItemRequestResponse, dependencies=[Depends(require_user)])
async def create_item_request(
    request_data: ItemRequestCreate,
    current_user: dict = Depends(require_user),
    db: Session = Depends(get_db)
):
    """
    Create new item request for unavailable item.
    
    Args:
        request_data: Item request details
        
    Returns:
        ItemRequestResponse: Created request
    """
    user_id = current_user["user_id"]
    
    item_request = ItemRequestService.create_request(db, user_id, request_data)
    
    return item_request


@router.get("/my-requests", response_model=dict, dependencies=[Depends(require_user)])
async def get_my_requests(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    status: str = Query(None),
    current_user: dict = Depends(require_user),
    db: Session = Depends(get_db)
):
    """
    Get current user's item requests.
    
    Args:
        skip: Number of requests to skip
        limit: Maximum requests to return
        status: Filter by status
        
    Returns:
        dict: Paginated request list
    """
    user_id = current_user["user_id"]
    
    total, requests = ItemRequestService.get_user_requests(db, user_id, skip, limit, status)
    
    return {
        "total": total,
        "page": skip // limit + 1 if limit > 0 else 1,
        "page_size": limit,
        "items": requests
    }


@router.get("/{request_id}", response_model=ItemRequestResponse, dependencies=[Depends(require_user)])
async def get_request(
    request_id: int,
    current_user: dict = Depends(require_user),
    db: Session = Depends(get_db)
):
    """
    Get item request details.
    
    Args:
        request_id: Request ID
        
    Returns:
        ItemRequestResponse: Request details
    """
    item_request = ItemRequestService.get_request(db, request_id)
    
    # Verify authorization
    user_id = current_user["user_id"]
    if item_request.user_id != user_id and current_user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this request"
        )
    
    return item_request


@router.get("/pending", response_model=dict)
async def get_pending_requests(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get pending item requests (admin/vendor view).
    
    Args:
        skip: Number of requests to skip
        limit: Maximum requests to return
        
    Returns:
        dict: Paginated pending request list
    """
    # Only admin and vendor can view pending requests
    if current_user["role"] not in ["admin", "vendor"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view pending requests"
        )
    
    total, requests = ItemRequestService.get_pending_requests(db, skip, limit)
    
    return {
        "total": total,
        "page": skip // limit + 1 if limit > 0 else 1,
        "page_size": limit,
        "items": requests
    }


@router.put("/{request_id}/status", response_model=ItemRequestResponse)
async def update_request_status(
    request_id: int,
    status_update: ItemRequestStatusUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update item request status (admin/vendor only).
    
    Args:
        request_id: Request ID
        status_update: New status
        
    Returns:
        ItemRequestResponse: Updated request
    """
    # Only admin and vendor can update request status
    if current_user["role"] not in ["admin", "vendor"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update request status"
        )
    
    return ItemRequestService.update_request_status(db, request_id, status_update)


@router.put("/{request_id}/assign-vendor/{vendor_id}", response_model=ItemRequestResponse)
async def assign_vendor(
    request_id: int,
    vendor_id: int,
    current_user: dict = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """
    Assign request to vendor (admin only).
    
    Args:
        request_id: Request ID
        vendor_id: Vendor ID to assign
        
    Returns:
        ItemRequestResponse: Updated request
    """
    return ItemRequestService.assign_to_vendor(db, request_id, vendor_id)


@router.put("/{request_id}/fulfill", response_model=ItemRequestResponse)
async def fulfill_request(
    request_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Mark request as fulfilled (vendor only).
    
    Args:
        request_id: Request ID
        
    Returns:
        ItemRequestResponse: Updated request
    """
    # Only vendor can fulfill requests
    if current_user["role"] != "vendor":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only vendors can fulfill requests"
        )
    
    return ItemRequestService.fulfill_request(db, request_id)
