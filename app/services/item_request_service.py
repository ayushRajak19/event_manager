"""
Item request service - Item request management business logic.
"""
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models import ItemRequest
from app.schemas.item_request import ItemRequestCreate, ItemRequestStatusUpdate


class ItemRequestService:
    """Service for item request operations."""

    @staticmethod
    def create_request(
        db: Session,
        user_id: int,
        request_data: ItemRequestCreate
    ) -> ItemRequest:
        """
        Create a new item request.
        
        Args:
            db: Database session
            user_id: User ID requesting the item
            request_data: Item request details
            
        Returns:
            ItemRequest: Created request
        """
        new_request = ItemRequest(
            user_id=user_id,
            item_name=request_data.item_name,
            description=request_data.description,
            category=request_data.category,
            status="pending"
        )
        
        db.add(new_request)
        db.commit()
        db.refresh(new_request)
        
        return new_request

    @staticmethod
    def get_request(db: Session, request_id: int) -> ItemRequest:
        """
        Get item request by ID.
        
        Args:
            db: Database session
            request_id: Request ID
            
        Returns:
            ItemRequest: Request object
            
        Raises:
            HTTPException: If request not found
        """
        request = db.query(ItemRequest).filter(ItemRequest.id == request_id).first()
        
        if not request:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Item request not found"
            )
        
        return request

    @staticmethod
    def get_user_requests(
        db: Session,
        user_id: int,
        skip: int = 0,
        limit: int = 10,
        status: str = None
    ) -> tuple:
        """
        Get user's item requests.
        
        Args:
            db: Database session
            user_id: User ID
            skip: Number of items to skip
            limit: Maximum items to return
            status: Filter by status
            
        Returns:
            tuple: (total_count, requests_list)
        """
        query = db.query(ItemRequest).filter(ItemRequest.user_id == user_id)
        
        if status:
            query = query.filter(ItemRequest.status == status)
        
        total = query.count()
        requests = query.order_by(ItemRequest.created_at.desc()).offset(skip).limit(limit).all()
        
        return total, requests

    @staticmethod
    def get_pending_requests(
        db: Session,
        skip: int = 0,
        limit: int = 10
    ) -> tuple:
        """
        Get all pending item requests (admin/vendor view).
        
        Args:
            db: Database session
            skip: Number of items to skip
            limit: Maximum items to return
            
        Returns:
            tuple: (total_count, requests_list)
        """
        query = db.query(ItemRequest).filter(ItemRequest.status == "pending")
        
        total = query.count()
        requests = query.order_by(ItemRequest.created_at.asc()).offset(skip).limit(limit).all()
        
        return total, requests

    @staticmethod
    def get_vendor_requests(
        db: Session,
        vendor_id: int,
        skip: int = 0,
        limit: int = 10,
        status: str = None
    ) -> tuple:
        """
        Get requests assigned to a vendor.
        
        Args:
            db: Database session
            vendor_id: Vendor ID
            skip: Number of items to skip
            limit: Maximum items to return
            status: Filter by status
            
        Returns:
            tuple: (total_count, requests_list)
        """
        query = db.query(ItemRequest).filter(ItemRequest.vendor_id == vendor_id)
        
        if status:
            query = query.filter(ItemRequest.status == status)
        
        total = query.count()
        requests = query.order_by(ItemRequest.created_at.desc()).offset(skip).limit(limit).all()
        
        return total, requests

    @staticmethod
    def update_request_status(
        db: Session,
        request_id: int,
        status_update: ItemRequestStatusUpdate
    ) -> ItemRequest:
        """
        Update item request status.
        
        Args:
            db: Database session
            request_id: Request ID
            status_update: New status and optional vendor assignment
            
        Returns:
            ItemRequest: Updated request
            
        Raises:
            HTTPException: If request not found
        """
        request = ItemRequestService.get_request(db, request_id)
        
        request.status = status_update.status
        if status_update.vendor_id:
            request.vendor_id = status_update.vendor_id
        
        db.commit()
        db.refresh(request)
        
        return request

    @staticmethod
    def assign_to_vendor(
        db: Session,
        request_id: int,
        vendor_id: int
    ) -> ItemRequest:
        """
        Assign a pending request to a vendor.
        
        Args:
            db: Database session
            request_id: Request ID
            vendor_id: Vendor ID
            
        Returns:
            ItemRequest: Updated request
            
        Raises:
            HTTPException: If request not found
        """
        request = ItemRequestService.get_request(db, request_id)
        
        request.vendor_id = vendor_id
        request.status = "approved"
        
        db.commit()
        db.refresh(request)
        
        return request

    @staticmethod
    def fulfill_request(
        db: Session,
        request_id: int
    ) -> ItemRequest:
        """
        Mark a request as fulfilled.
        
        Args:
            db: Database session
            request_id: Request ID
            
        Returns:
            ItemRequest: Updated request
            
        Raises:
            HTTPException: If request not found
        """
        request = ItemRequestService.get_request(db, request_id)
        
        request.status = "fulfilled"
        
        db.commit()
        db.refresh(request)
        
        return request
